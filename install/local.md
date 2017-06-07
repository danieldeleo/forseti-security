---
install_type: 'local'
permalink: /install/local/
---
# Local installation
## Prerequisites
{% include install_prerequisites.md %}
{% include install_local_prerequisites.md %}

## Create a virtualenv
```sh
$ mkvirtualenv forseti-security
$ workon forseti-security
```

## Get the source code
Clone the repo, if you haven't already done so.

```sh
$ git clone https://github.com/GoogleCloudPlatform/forseti-security.git
```

## Run the python setup
Navigate to your cloned repo, then run:

```sh
$ python setup.py install
```

## Execution
You should now be able to run the following commandline tools. To see the flag options for each, use
the `--helpshort` or `--helpfull` flags.

 * [`forseti_inventory`]({{ site.baseurl }}{% link modules/core/inventory/index.md %})
 * [`forseti_scanner`]({{ site.baseurl }}{% link modules/core/scanner/index.md %})
 * [`forseti_enforcer`]({{ site.baseurl }}{% link modules/core/enforcer/index.md %})