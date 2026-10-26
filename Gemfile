source "https://rubygems.org"

# This pins your local Jekyll version to whatever GitHub Pages actually
# runs in production, so "works on my machine" == "works when pushed".
gem "github-pages", group: :jekyll_plugins

gem "jekyll-feed"

# Windows/JRuby support (harmless to leave in even if you're not on either)
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]
