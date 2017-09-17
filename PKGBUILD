pkgname=dataleech
pkgdesc='Dataleech - a backup plan using ZFS...'
pkgver=0.9
pkgrel=1
arch=('x86_64')
url='https://github.com/xvzf/dataleech'
license=('GPL3')
depends=('zfs-utils' 'python' 'pv' 'openssh' 'cronie')
makedepends=('bazel')
provides=('newcustomsnap' 'superman' 'snapsync')
backup=('etc/dataleech/datasets')

build() {
    cd "${srcdir}"
    bazel build '...'

    # Remove manifests
    cd ./bazel-bin/snapmanager
    for i in $(find . -name MANIFEST -type f); do
        echo "Deleting $i"
        rm -f $i
    done
}

package() {
    mkdir -p "${pkgdir}/usr/libexec/dataleech/"
    mkdir -p ${pkgdir}/etc/{dataleech,cron.d}


    for i in $(echo newdailysnap newshortsnap newcustomsnap newweeklysnap snapsync)
    do
        chmod 755 "${srcdir}/bazel-bin/snapmanager/${i}"
        sed "s#os.path.abspath(sys.argv\[0\])#'/usr/libexec/dataleech/${i}'#g" -i "${srcdir}/bazel-bin/snapmanager/${i}"

        install -Dm755 "${srcdir}/bazel-bin/snapmanager/${i}" "${pkgdir}/usr/bin/${i}"

          # install -d just doesnt work for that many files
        cp -L -r "${srcdir}/bazel-bin/snapmanager/${i}.runfiles" "${pkgdir}/usr/libexec/dataleech/${i}.runfiles"
        chmod 755 -R "${pkgdir}/usr/libexec/dataleech/"
    done

    mv "${pkgdir}/usr/bin/newshortsnap"						"${pkgdir}/usr/libexec/dataleech/newshortsnap"
    mv "${pkgdir}/usr/bin/newdailysnap"						"${pkgdir}/usr/libexec/dataleech/newdailysnap"
    mv "${pkgdir}/usr/bin/newweeklysnap"					"${pkgdir}/usr/libexec/dataleech/newweeklysnap"
    install -Dm644 "${srcdir}/bazel-genfiles/configfiles/datasets"		"${pkgdir}/etc/dataleech/datasets"
    install -Dm644 "${srcdir}/bazel-genfiles/cronfiles/dataleech"		"${pkgdir}/etc/cron.d/dataleech"
    install -Dm755 "${srcdir}/bazel-genfiles/cronfiles/dataleech_daily"		"${pkgdir}/etc/cron.daily/dataleech"
    install -Dm755 "${srcdir}/bazel-genfiles/cronfiles/dataleech_weekly"	"${pkgdir}/etc/cron.weekly/dataleech"
    install -Dm755 "${srcdir}/bazel-genfiles/archscripts/superman"		"${pkgdir}/usr/bin/superman"
}

# vim:set ts=8 sts=2 sw=2 et:
