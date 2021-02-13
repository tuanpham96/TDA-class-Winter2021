function Para(el) 
  if el.content[1].text == "{%" then
    return pandoc.Str ""
  end
end
