## Installation

### Homebrew
Once [homebrew](https://brew.sh/) is installed, run the following:

```
brew tap unsupported/canvas/other/inst-api
brew install inst-api
```

### Download

[Download](https://github.com/unsupported/canvas/other/inst-api/releases) or clone the latest release and symlink the scripts to a location supported in your `$PATH`

## Dependencies
The included scripts require the following dependencies.  The scripts will attempt to install `npm` and `pip` dependencies if they're not found. System or built-in commands must be installed by the user.

Not all scripts use all dependencies, but they will all ensure that their specific dependencies are met. E.g. `bridge` requires `python` but `canvas` does not, therefore `canvas` will not check for `python`.

### System / Built-in
* [curl](https://curl.haxx.se/)
* [sed](https://www.gnu.org/software/sed/)
* [cut](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/cut.html)
* [getopts](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/getopts.html)
* [python](https://www.python.org/)

### External
* [json](https://www.npmjs.com/package/json) ([npm](https://www.npmjs.com/))
* [pygments](http://pygments.org/) ([pip](https://pypi.python.org/pypi))

## Security

### Credentials
All commands store credentials in a dot file in the user home directory, specifically `~/.inst` and they source the contents at runtime.  **DO NOT** store your tokens or credentials on a shared machine or user space.  If security is a concern, all commands allow you to pass credentials in via options at runtime using `-t <token>` or `-p <password>`.  This allows you to use other credential managers like [vaulted](https://github.com/miquella/vaulted).  See help (`-h`) for more information with each command.

### Encryption
All `curl` commands use the `--tlsv1.2` flag and all paths explicitly start with `https`.  If your machine does not support TLS v1.2, downgrade at your own risk.  Instructure products **WILL NOT** function over `http` except to redirect to `https`.  
