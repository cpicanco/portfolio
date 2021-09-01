# install

  # ruby
  # https://github.com/postmodern/ruby-install#readmes
  ruby-install ruby

  # ~/.bashrc
  # export PATH="${PATH}:${HOME}/.rubies/ruby-2.2.3/bin"

  # install ruby gems
  cd ~
  cd Downloads/
  wget https://rubygems.org/rubygems/rubygems-x.tgz
  tar xvf rubygems-x.tgz
  cd rubygems-x
  ruby setup.rb

  # install bundler gem
  gem install bundler

  # install github pages/jekyll
  # https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/
  cd ~
  cd git/
  git clone https://github.com/cpicanco/portfolio.git
  cd portfolio
  bundle install

  # optional 
    # install npm
    sudo apt-get install npm

    # grunt
    sudo npm install -g grunt-cli
    ln -s /usr/bin/nodejs /usr/bin/node #ubuntu
  
    # libZotero
    sudo pip install libZotero

    # citeproc-py
    sudo apt-get install python-lxml python3-lxml
    sudo pip install citeproc-py

    # grunt dependencies
    npm install

# tasks
  # fecth new publications when necessary
    python fetch_publication.py #ctrl+b ;)

  # test html
    bundle exec htmlproofer ./_site --disable-external --allow-hash-href  

# misc

  # update github-pages dependencies
  bundle update
  
  # new task
  npm install <task-name> --save-dev

  # serve github page
  bundle exec jekyll serve