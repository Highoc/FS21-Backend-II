# bootstrap-chosen (sass)

![](https://github.com/Dinu/bootstrap-chosen/raw/master/example.png)

An alternate stylesheet for [Chosen 1.0](http://harvesthq.github.com/chosen/). Fork of [Alxlit's repo](https://github.com/alxlit/bootstrap-chosen) to integrate better with [Bootstrap 4-alpha2](http://v4-alpha.getbootstrap.com/).

[Here's the example page](http://Dinu.github.io/bootstrap-chosen/).

How you add `bootstrap-chosen.scss` to your build process is up to you. Just keep
in mind that it needs access to `variables.scss` and `mixins.scss`.

You can tinker with the example page by:

```
$ git clone https://github.com/Dinu/bootstrap-chosen
$ cd bootstrap-chosen
bootstrap-chosen $ git clone --depth=1 --branch v4-dev https://github.com/twbs/bootstrap.git
bootstrap-chosen $ vi bootstrap/scss/bootstrap.scss

// Add this to the bottom
@import "../../bootstrap-chosen.scss";

bootstrap-chosen $ sass bootstrap/scss/bootstrap.scss bootstrap.css
bootstrap-chosen $ firefox example.html
```

License: [MIT](https://en.wikipedia.org/wiki/MIT_License)

