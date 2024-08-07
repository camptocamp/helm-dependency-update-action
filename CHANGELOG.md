# Changelog

## [0.5.0](https://github.com/camptocamp/helm-dependency-update-action/compare/v0.4.1...v0.5.0) (2024-08-07)


### Features

* update Upgrade CLI and other dependencies ([0d58dad](https://github.com/camptocamp/helm-dependency-update-action/commit/0d58daddc47f2c4012c9a06ab061dafa8ad104b5))

## [0.4.1](https://github.com/camptocamp/helm-dependency-update-action/compare/v0.4.0...v0.4.1) (2023-08-09)


### Bug Fixes

* add support for charts indexes containing the v prefix in version ([#16](https://github.com/camptocamp/helm-dependency-update-action/issues/16)) ([ca7538a](https://github.com/camptocamp/helm-dependency-update-action/commit/ca7538a308b6a6f92aec038ba3f5c15999ae47da))

## [0.4.0](https://github.com/camptocamp/helm-dependency-update-action/compare/v0.3.3...v0.4.0) (2023-07-14)


### ⚠ BREAKING CHANGES

* change the naming scheme

### Features

* change the naming scheme ([c321a12](https://github.com/camptocamp/helm-dependency-update-action/commit/c321a12801f41b210685122ce1c5f1c1918388a9))

## [0.3.3](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.3.2...v0.3.3) (2023-07-14)


### Bug Fixes

* always output even if in dry-run ([5475c56](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/5475c563119347e1c563a8c6090ab1f7d3b4c5dc))

## [0.3.2](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.3.1...v0.3.2) (2023-07-14)


### Bug Fixes

* add management of empty exclusion variable ([7f1dea5](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/7f1dea5cb8cbe21d2a8331b799d58ba36ea99e30))

## [0.3.1](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.3.0...v0.3.1) (2023-07-14)


### Bug Fixes

* add missing output to the action.yaml ([db220be](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/db220be7f54112bfeb66b61f4fca5658b05af837))

## [0.3.0](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.2.1...v0.3.0) (2023-07-14)


### Features

* rework the output to consider all cases in a single output ([fd5a89b](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/fd5a89b69cd6275b5de8aeb8032ae45bcbb741c6))


### Bug Fixes

* add sort to the attribute function and small cleanup ([13f351f](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/13f351f1ec696a5366d8044d64036809523bc36a))
* correct the function to output new versions to README.adoc ([c88c25b](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/c88c25bb2c75f9b43fe28b82539abf6cea1816ce))

## [0.2.1](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.2.0...v0.2.1) (2023-07-13)


### Bug Fixes

* remove separate line for description ([b8e1934](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/b8e193439fb9a95e62d87862cf31a4f95128b30b))

## [0.2.0](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.1.5...v0.2.0) (2023-07-13)


### Features

* add support to generate outputs and update README.adoc ([87c5777](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/87c5777559c46e88881fd148e698644c272e2fe3))

## [0.1.5](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.1.4...v0.1.5) (2023-07-05)


### Bug Fixes

* revert "fix: remove the output as it was posing more problems than solutions" ([2719816](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/27198169a677216b417125430463d450b82b82f8))

## [0.1.4](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.1.3...v0.1.4) (2023-07-05)


### Bug Fixes

* remove the output as it was posing more problems than solutions ([cf7637d](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/cf7637dc1906577e377848e9fc66223a60a7c5be))

## [0.1.3](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.1.2...v0.1.3) (2023-07-05)


### Bug Fixes

* fix git issue with file ownership inside the workspace ([9db06d0](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/9db06d082875471a70e822a50d7184473230e315))

## [0.1.2](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.1.1...v0.1.2) (2023-07-05)


### Bug Fixes

* correct error correction condition in entrypoint.sh ([26ac098](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/26ac098a3629992745ef1635112420d4aea1054f))

## [0.1.1](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.1.0...v0.1.1) (2023-07-05)


### Bug Fixes

* fix update entrypoint.sh ([8d78cf3](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/8d78cf365e26ba4ed20a7c27eb189bc011c44906))

## [0.1.0](https://github.com/camptocamp/helm-dependency-upgrade-action/compare/v0.0.1...v0.1.0) (2023-07-04)


### Features

* small changes to docs and renamed output ([7c927f2](https://github.com/camptocamp/helm-dependency-upgrade-action/commit/7c927f27c3160c019050195b8d0d59b42f074978))

## 0.0.1 (2023-07-04)


### Features

* add first draft ([19f2763](https://github.com/lentidas/helm-dependency-upgrade-action/commit/19f27638aebc545607fae7d50ce7e5ada7066347))
* add program arguments ([b1a153f](https://github.com/lentidas/helm-dependency-upgrade-action/commit/b1a153f00146b45c8a3b85723a2e703a69f3d84e))
* small improvements ([0e6572f](https://github.com/lentidas/helm-dependency-upgrade-action/commit/0e6572f432016c095081dfc8f0751125a25dd0a1))
* update the Python script and add first iteration of the action ([d957254](https://github.com/lentidas/helm-dependency-upgrade-action/commit/d957254dd720e566125ca7737b6ecc0be4a1eeb0))
