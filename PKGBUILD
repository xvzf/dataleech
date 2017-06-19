pkgname=dataleech
pkgdesc='Dataleech - a backup plan using ZFS...'
pkgver=0.2
pkgrel=3
arch=('x86_64')
url='https://github.com/xvzf/dataleech'
license=('GPL3')
depends=('python' 'mbuffer')
makedepends=('bazel')
provides=('newshortsnap' 'newdailysnap' 'newcustomsnap' 'superman')
backup=('etc/dataleech/datasets' 'remoteoptions')

build() {
  cd "${srcdir}"
  bazel build '...'
}

package() {
  mkdir -p "${pkgdir}/usr/libexec/dataleech/"
  for i in $(echo newdailysnap newshortsnap newcustomsnap confreader)
  do
	chmod 755 "${srcdir}/bazel-bin/snapmanager/${i}"
	sed "s#os.path.abspath(sys.argv\[0\])#'/usr/libexec/dataleech/${i}'#g" -i "${srcdir}/bazel-bin/snapmanager/${i}"

	install -Dm755 "${srcdir}/bazel-bin/snapmanager/${i}" "${pkgdir}/usr/bin/${i}"

	  # install -d just doesnt work for that many files
	cp -L -r "${srcdir}/bazel-bin/snapmanager/${i}.runfiles" "${pkgdir}/usr/libexec/dataleech/${i}.runfiles" 
	chmod 755 -R "${pkgdir}/usr/libexec/dataleech/"
  done

  mv ${pkgdir}/usr/bin/confreader ${pkgdir}/usr/libexec/dataleech/confreader

  mkdir -p ${pkgdir}/etc/{dataleech,cron.d}

  install -Dm644 "${srcdir}/bazel-genfiles/configfiles/datasets" "${pkgdir}/etc/dataleech/datasets"
  install -Dm644 "${srcdir}/bazel-genfiles/configfiles/remoteoptions" "${pkgdir}/etc/dataleech/remoteoptions"
  install -Dm644 "${srcdir}/bazel-genfiles/cronfiles/dataleech" "${pkgdir}/etc/cron.d/dataleech" 
  install -Dm755 "${srcdir}/bazel-genfiles/cronfiles/dataleech_daily" "${pkgdir}/etc/cron.daily/dataleech"
  install -Dm755 "${srcdir}/bazel-genfiles/archscripts/snapsend" "${pkgdir}/usr/libexec/dataleech/snapsend"
  install -Dm755 "${srcdir}/bazel-genfiles/archscripts/snapreceive" "${pkgdir}/usr/libexec/dataleech/snapreceive"
  install -Dm755 "${srcdir}/bazel-genfiles/archscripts/superman" "${pkgdir}/usr/bin/superman"
  install -Dm755 "${srcdir}/bazel-genfiles/archscripts/snapsync" "${pkgdir}/usr/bin/snapsync"
}
