# Working as of 02/21/2019
class InstApi < Formula
  desc "A collection of wrappers for Instructure APIs"
  homepage "https://github.com/unsupported/canvas/other/inst-api"
  url "https://github.com/thedannywahl/inst-api/archive/v0.3.1.zip"
  sha256 "9b8135aa0871df7d5fba0d28a5a1fcc1187632c02c765d6f41ba33ed5e1ec3fc"

  def install
    bin.install Dir["arc/arc"], Dir["bridge/bridge"], Dir["canvas/canvas"], Dir["catalog/catalog"], Dir["commons/commons"]
  end

  def caveats; <<~EOS
      Installed binaries are: arc, bridge, canvas, catalog, commons
      User pref file is stored in ~/.inst
  EOS
  end

  test do
    system "#{bin}/arc -v"
    system "#{bin}/bridge -v"
    system "#{bin}/canvas -v"
    system "#{bin}/catalog -v"
    system "#{bin}/commons -v"
  end

end
