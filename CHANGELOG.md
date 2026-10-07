# Changelog

## 0.2.0

- Build wheels against a pinned ICU 78.3 instead of the build image's ICU 60
  - ICU 60 is AlmaLinux 8's, carrying CLDR 32 from 2017
  - Fixes `sw`, `lb`, `ne`, `kk`, `su`, `qu`, `ff` and `ccp`, which had no rules in ICU 60 and silently spelled numbers in English
  - Corrects `da`, `bg`, `ar`, `ro`, `ca`, `hu`, `nn`, `lt` and `id`
- Add `icu_version()`, and a test asserting ICU >= 77

## 0.1.0

- Initial version
