# Packaging and Build Farm Setup for MBASIC

⏳ **Status**: TODO - Research Complete

## Overview

Setup automated multi-architecture package building for MBASIC using free/open-source build farms. Target formats: `.deb` (Debian/Ubuntu), `.snap`, and potentially AppImage/Flatpak.

## Target Architectures

**Priority Architectures:**
- `amd64` (x86_64) - Primary desktop/laptop
- `arm64` (aarch64) - Raspberry Pi 4/5, Apple Silicon, servers
- `armhf` (armv7) - Raspberry Pi 3, older ARM devices

**Lower Priority:**
- `i386` (x86 32-bit) - Legacy systems
- `ppc64el` (PowerPC 64-bit) - IBM POWER systems
- `s390x` - IBM Z mainframes
- `riscv64` - Emerging RISC-V systems

## Free Build Farm Options

### Option 1: Launchpad (Ubuntu PPAs) ⭐ RECOMMENDED for .deb

**Website:** https://launchpad.net/

**Pros:**
- ✅ FREE for open source projects
- ✅ Official Ubuntu infrastructure (399+ build machines as of 2025)
- ✅ Multi-architecture support: amd64, arm64, armhf, i386, ppc64el, s390x, riscv64
- ✅ Automatic PPA hosting - users just add PPA and `apt install`
- ✅ Builds for multiple Ubuntu versions (22.04, 24.04, etc.)
- ✅ Well-documented, mature platform
- ✅ Works for Debian too (with some tweaks)

**Cons:**
- ❌ Requires GPG key setup
- ❌ Must sign Ubuntu Code of Conduct
- ❌ Learning curve for source package format
- ❌ Ubuntu-focused (but packages work on Debian)

**Setup Requirements:**
1. Create Launchpad account (https://launchpad.net/)
2. Generate and register GPG key
3. Sign Ubuntu Code of Conduct
4. Create PPA (Personal Package Archive)
5. Build source package with `debuild -S`
6. Upload with `dput`

**Distribution:**
```bash
# Users add PPA
sudo add-apt-repository ppa:your-username/mbasic
sudo apt update
sudo apt install mbasic
```

**Resources:**
- Tutorial: https://help.launchpad.net/Packaging/PPA
- Build farm status: https://launchpad.net/builders/
- Source package guide: https://saveriomiroddi.github.io/Building-a-debian-deb-source-package-and-publishing-it-on-an-ubuntu-ppa/

---

### Option 2: GitHub Actions + Snapcraft ⭐ RECOMMENDED for Snap

**Website:** https://github.com/features/actions

**Pros:**
- ✅ FREE for public repos (2000 minutes/month, unlimited for public repos)
- ✅ FREE native ARM64 runners (as of Jan 2025!)
- ✅ Multi-arch support with QEMU or native
- ✅ Snapcraft multiarch action available
- ✅ Direct integration with GitHub repo
- ✅ Auto-publish to Snap Store
- ✅ Matrices for parallel builds

**Cons:**
- ❌ Requires Snapcraft account for publishing
- ❌ QEMU builds slower than native
- ❌ Monthly minute limits (though generous)

**Key Actions:**
- `diddlesnaps/snapcraft-multiarch-action` - Multi-arch snap builds
- `docker/setup-qemu-action` - QEMU for cross-compilation
- `snapcraftio/action-publish` - Auto-publish to Snap Store

**Example Workflow:**

```yaml
name: Build Snap Packages

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        architecture: [amd64, arm64, armhf]

    steps:
      - uses: actions/checkout@v4

      - name: Setup QEMU
        uses: docker/setup-qemu-action@v3

      - name: Build Snap
        uses: diddlesnaps/snapcraft-multiarch-action@v1
        with:
          architecture: ${{ matrix.architecture }}

      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: mbasic-${{ matrix.architecture }}.snap
          path: '*.snap'

      - name: Publish to Snap Store
        if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/')
        uses: snapcraftio/action-publish@v1
        env:
          SNAPCRAFT_STORE_CREDENTIALS: ${{ secrets.SNAPCRAFT_TOKEN }}
        with:
          snap: '*.snap'
          release: stable
```

**Distribution:**
```bash
# Users install from Snap Store
sudo snap install mbasic
```

**Resources:**
- GitHub Actions: https://github.com/features/actions
- Snapcraft Action: https://github.com/marketplace/actions/snapcraft-multiarch-build
- ARM64 runners: https://github.blog/changelog/2025-01-16-arm64-linux-and-windows-runners-are-now-available-in-github-actions/

---

### Option 3: Open Build Service (OBS) - Multi-distro

**Website:** https://build.opensuse.org/

**Pros:**
- ✅ FREE for open source
- ✅ Builds for many distros: openSUSE, Fedora, Debian, Ubuntu, Arch, etc.
- ✅ Multi-architecture support
- ✅ One source, many targets
- ✅ Repository hosting included

**Cons:**
- ❌ More complex setup than Launchpad
- ❌ openSUSE-centric (but supports others)
- ❌ Steeper learning curve

**Use Case:** If you want packages for Fedora, openSUSE, etc. in addition to Ubuntu/Debian.

---

### Option 4: GitHub Actions + Debian Build

**Setup:** Use GitHub Actions to build `.deb` directly

**Pros:**
- ✅ Full control over build process
- ✅ Can build for specific Debian/Ubuntu versions
- ✅ Artifacts stored on GitHub Releases

**Cons:**
- ❌ No automatic repository hosting
- ❌ Users must manually download `.deb`
- ❌ More manual work than Launchpad PPA

**Example Workflow:**

```yaml
name: Build Debian Package

on:
  push:
    tags:
      - 'v*'

jobs:
  build-deb:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        arch: [amd64, arm64]

    steps:
      - uses: actions/checkout@v4

      - name: Setup build environment
        run: |
          sudo apt-get update
          sudo apt-get install -y debhelper devscripts

      - name: Build package
        run: |
          dpkg-buildpackage -us -uc -a${{ matrix.arch }}

      - name: Upload to Release
        uses: softprops/action-gh-release@v1
        with:
          files: ../*.deb
```

---

## Recommended Approach for MBASIC

### Phase 1: Snap Package (Quick Win) 🎯

**Why Start Here:**
1. Easiest to set up (single `snapcraft.yaml`)
2. Free GitHub Actions with ARM64 support
3. Auto-updates for users
4. Cross-distro support (Ubuntu, Debian, Fedora, Arch, etc.)
5. Sandboxed and secure

**Timeline:** 1-2 days

**Steps:**
1. Create `snap/snapcraft.yaml`
2. Setup GitHub Actions workflow
3. Register on Snapcraft.io
4. Auto-publish on tag push

---

### Phase 2: Ubuntu PPA (Debian/Ubuntu Native) 🎯

**Why Next:**
1. Native package manager integration
2. Better for servers (no snap daemon needed)
3. Debian/Ubuntu users prefer `.deb`
4. Launchpad provides free build farm + hosting

**Timeline:** 3-5 days (includes learning curve)

**Steps:**
1. Create Debian packaging files (`debian/` directory)
2. Setup Launchpad account and GPG
3. Create PPA
4. Document upload process
5. Setup automation (GitHub Action → source package → Launchpad)

---

### Phase 3: AppImage (Optional) 🔮

**Why Consider:**
- Works on any Linux distro
- No installation needed (portable)
- Single file distribution

**Tools:**
- `python-appimage` or `appimage-builder`
- Can build with GitHub Actions

---

## Package Format Comparison

| Feature | Snap | .deb (PPA) | AppImage | Flatpak |
|---------|------|------------|----------|---------|
| **Distribution** | Snap Store | PPA/apt | Direct download | Flathub |
| **Auto-updates** | ✅ Yes | ✅ Yes (apt) | ❌ No | ✅ Yes |
| **Sandboxing** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Multi-distro** | ✅ Yes | ⚠️ Ubuntu/Debian | ✅ Yes | ✅ Yes |
| **Dependencies** | Bundled | System | Bundled | Bundled |
| **Size** | Medium | Small | Large | Large |
| **Startup Speed** | Fast | Fastest | Fast | Medium |
| **Ease of Creation** | Easy | Medium | Medium | Medium |

---

## Implementation Checklist

### For Snap Package

- [ ] Create `snap/snapcraft.yaml`
  ```yaml
  name: mbasic
  version: '1.0.111'
  summary: MBASIC 5.21 compatible BASIC interpreter
  description: |
    Modern implementation of Microsoft MBASIC 5.21 with enhanced
    features including TK GUI, case-preserving variables, and more.

  base: core22
  confinement: strict
  grade: stable

  apps:
    mbasic:
      command: bin/mbasic
      plugs: [home, network]

  parts:
    mbasic:
      plugin: python
      source: .
      requirements: [requirements.txt]
      python-packages:
        - .
  ```

- [ ] Setup GitHub Actions workflow (see template above)
- [ ] Register Snapcraft account
- [ ] Generate Snapcraft token: `snapcraft export-login snapcraft-token.txt`
- [ ] Add `SNAPCRAFT_TOKEN` to GitHub Secrets
- [ ] Test build locally: `snapcraft`
- [ ] Push tag to trigger build: `git tag v1.0.111 && git push --tags`
- [ ] Verify on Snap Store

### For Debian/Ubuntu PPA

- [ ] Create `debian/` directory structure
  - [ ] `debian/control` - Package metadata
  - [ ] `debian/rules` - Build rules
  - [ ] `debian/changelog` - Version history
  - [ ] `debian/copyright` - License info
  - [ ] `debian/compat` - Debhelper compat level
  - [ ] `debian/install` - File installation rules

- [ ] Setup Launchpad account
- [ ] Generate GPG key: `gpg --gen-key`
- [ ] Upload key to Ubuntu keyserver: `gpg --send-keys YOUR_KEY_ID`
- [ ] Sign Ubuntu Code of Conduct
- [ ] Create PPA on Launchpad
- [ ] Test local build: `debuild -S`
- [ ] Upload: `dput ppa:username/mbasic mbasic_1.0.111_source.changes`
- [ ] Document for users: Add PPA instructions to README

### For GitHub Release .deb

- [ ] Create GitHub Actions workflow for .deb
- [ ] Test multi-arch builds (amd64, arm64)
- [ ] Auto-upload to GitHub Releases on tag
- [ ] Update README with download instructions

---

## Documentation Updates Needed

1. **Installation Guide** (`docs/user/INSTALLATION.md`)
   - Add Snap installation instructions
   - Add PPA installation instructions
   - Add manual .deb installation

2. **README.md**
   - Add "Installation" section with badges
   - Snap Store badge
   - PPA instructions

3. **CONTRIBUTING.md**
   - Document package build process
   - How to test packages locally

---

## Resources and References

### Snap Resources
- **Snapcraft Python Apps**: https://snapcraft.io/docs/python-apps
- **Multiarch Action**: https://github.com/marketplace/actions/snapcraft-multiarch-build
- **GitHub ARM64 Runners**: Free as of Jan 2025

### Launchpad Resources
- **PPA Guide**: https://help.launchpad.net/Packaging/PPA
- **Build Farm**: https://launchpad.net/builders/
- **Source Package Tutorial**: https://saveriomiroddi.github.io/Building-a-debian-deb-source-package-and-publishing-it-on-an-ubuntu-ppa/

### Debian Packaging
- **New Maintainer's Guide**: https://www.debian.org/doc/manuals/maint-guide/
- **Python Debian Packaging**: https://wiki.debian.org/Python/Packaging

---

## Estimated Timeline

| Phase | Effort | Timeline |
|-------|--------|----------|
| **Snap Package** | Low | 1-2 days |
| **GitHub Actions Setup** | Low | 1 day |
| **Launchpad PPA** | Medium | 3-5 days |
| **Documentation** | Low | 1 day |
| **Testing** | Low | 1 day |
| **TOTAL** | | **1-2 weeks** |

---

## Priority

**Medium-High** - Packaging greatly improves accessibility and distribution

## Benefits

1. **Professional distribution** - Users can install with package manager
2. **Auto-updates** - Users get latest version automatically
3. **Multi-architecture** - Works on Raspberry Pi, desktops, servers
4. **Wider adoption** - Easier installation = more users
5. **Credibility** - Official packages signal maturity

## Next Steps

1. Create `snap/snapcraft.yaml` (start simple)
2. Test local snap build: `snapcraft`
3. Setup GitHub Actions for multi-arch
4. Register on Snapcraft.io
5. Publish first snap release
6. Move to Debian packaging (Phase 2)

---

## Notes

- All build farms listed are **FREE** for open source
- GitHub Actions provides **unlimited** minutes for public repos
- ARM64 native builds now free on GitHub (huge win!)
- Snap is cross-distro (works on Ubuntu, Debian, Fedora, Arch, etc.)
- PPA is Ubuntu/Debian specific but better native integration
- MBASIC is pure Python - makes packaging easier than compiled apps
