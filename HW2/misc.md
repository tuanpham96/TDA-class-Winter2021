# Misc notes

For `gudhi` package, if want to use `latex` in `matplotlib`, might need to might need to do: `sudo apt-get install dvipng texlive-latex-extra texlive-fonts-recommended cm-super` (if `tex` is built not in the normal way and in some user defined custom paths and somehow `matplotlib` couldn't find the right path and too lazy to figure out). Additionally, 2 more things to do, just in case:

- 
``` python
import matplotlib.font_manager
matplotlib.font_manager._rebuild()
```
- clearing cache: `rm -rf ~/.cache/matplotlib/*`

Otherwise: do this to disable `latex` rendering in `matplotlib` used by [`gudhi`](https://gudhi.inria.fr/python/latest/installation.html#latex):

``` python
import gudhi
gudhi.persistence_graphical_tools._gudhi_matplotlib_use_tex=False
```