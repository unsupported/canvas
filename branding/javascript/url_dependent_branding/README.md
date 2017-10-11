# Loading Specific Branding Dependent on Canvas URL

This folder is used to load styling dependent on the ```javascript window.location.hostname```, which can be useful if you have multiple domains for a single Canvas instance, or you're utilizing a vanity URL.

# Edits to Make Prior to Using

1. Each `case` will need a single URL, either <DOMAIN>.instructure.com or your vanity URL.
2. Add your styling to this line, replacing the REPLACE_ME as your placeholder `sheet.innerHTML = "{REPLACE_ME}";`
