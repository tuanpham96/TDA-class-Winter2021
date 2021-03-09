%% Prepocess raw F data to dF/F0
% NOTE: the raw data mat files are from Silas, combined and prepoccesed in 
% "purkpop-calcium-silas.mat" file, NOT included in version control 
clc; clear; 
data_path = '../data'; 
raw_data_path = fullfile(data_path, 'raw'); 
preproc_data_path = fullfile(data_path, 'preprocessed'); 

preprocessd_filename = 'purkpop-dFF0.mat';
src_filepattern = '*analysis.mat';

info = struct; 
info.description = 'Calcium imaging of Purkinje cell population'; 
info.experimenter = 'Silas Busch, Ting-Feng Lin, Christian Hansel'; 
info.data_source = '012_018_XXX_OUT_MotCor ROI analysis.mat';
info.Fs = 60; % Hz 
info.T = 20; % s 
info.t_stim = 10; % s 

%% Start prepocessing through each file 
dat_files = dir(fullfile(raw_data_path, src_filepattern)); 
dat_files = {dat_files.name}; 

num_trials = length(dat_files);

dF_F0 = cell(num_trials, 1); 
trial_ids = zeros(num_trials, 1); 

for i = 1:num_trials 
    fn = fullfile(raw_data_path, dat_files{i}); 
    split_fn = strsplit(dat_files{i}, '_'); 
    trial_ids(i) = str2double(split_fn{3}); 
    dat = load(fn, 'activs');
    [dF_F0{i}, preprocess_description] = preprocess_fluorescence_data(dat.activs);
end

info.preprocess = preprocess_description;

%% Saving
save(fullfile(preproc_data_path, preprocessd_filename), ...
    'dF_F0', 'info', 'trial_ids');

%% Functions
function [dF_F0, description] = preprocess_fluorescence_data(raw_F,med_win,prc4base,sm_win,sm_meth)
if ~exist('med_win', 'var'), med_win = 10; end 
if ~exist('prc4base', 'var'), prc4base = 5; end
if ~exist('sm_win', 'var'), sm_win = 10; end 
if ~exist('sm_meth', 'var'), sm_meth = 'gauss'; end 

F = smoothdata(raw_F, 1, 'movmedian', med_win); 
F0 = prctile(F, prc4base, 1);
dF_F0 = (F - F0) ./ F0; 

description = sprintf('smoothdata(MOVMEDIAN, %d pnts)\n[ (F-F0)/F0 ] (F0=%.1f-th percentile)',med_win,prc4base);
if sm_win < 1 || strcmpi(sm_meth, 'none')
    return; 
end

dF_F0 = smoothdata(dF_F0, 1, sm_meth, sm_win); 
description = sprintf('%s\nsmoothdata(%s, %d pnts)', description, upper(sm_meth), sm_win); 
end