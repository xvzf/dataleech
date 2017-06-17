pkgname=dataleech
pkgdesc=''
pkgver=0.1
pkgrel=2
arch=('x86_64')
url='https://github.com/xvzf/dataleech'
license=('GPL3')
depends=('python')
makedepends=('bazel')
provides=('newshortsnap' 'newdailysnap' 'newcustomsnap' 'superman')
backup=('etc/dataleech/datasets')

build() {
  cd "${srcdir}"
  bazel build '...'
}

package() {
  mkdir -p "${pkgdir}/usr/libexec/dataleech/"
  for i in $(echo newdailysnap newshortsnap newcustomsnap)
  do
	chmod 755 "${srcdir}/bazel-bin/snapmanager/${i}"
	
	sed "s#os.path.abspath(sys.argv\[0\])#'/usr/libexec/dataleech/${i}'#g" -i "${srcdir}/bazel-bin/snapmanager/${i}"

	install -Dm755 "${srcdir}/bazel-bin/snapmanager/${i}" "${pkgdir}/usr/bin/${i}"

	  # install -d just doesnt work for that many files
	cp -L -r "${srcdir}/bazel-bin/snapmanager/${i}.runfiles" "${pkgdir}/usr/libexec/dataleech/${i}.runfiles" 
	chmod 755 -R "${pkgdir}/usr/libexec/dataleech/"
  done

  mkdir -p ${pkgdir}/etc/{dataleech,cron.d}

  install -Dm644 "${srcdir}/bazel-genfiles/configfiles/datasets" "${pkgdir}/etc/dataleech/datasets"
  install -Dm644 "${srcdir}/bazel-genfiles/cronfiles/dataleech" "${pkgdir}/etc/cron.d/dataleech" 
  install -Dm755 "${srcdir}/bazel-genfiles/cronfiles/dataleech_daily" "${pkgdir}/etc/cron.daily/dataleech"

  install -Dm755 "${srcdir}/bazel-genfiles/archscripts/superman" "${pkgdir}/usr/bin/superman"
}

