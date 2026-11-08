// usage: rendercrop pdf pageIndex scale x0 y0 x1 y1 out.png   (crop in top-left page points)
import PDFKit
import AppKit
let a = CommandLine.arguments
let d = PDFDocument(url: URL(fileURLWithPath: a[1]))!
let p = d.page(at: Int(a[2])!)!
let b = p.bounds(for: .mediaBox)
let s = CGFloat(Double(a[3])!)
let x0 = CGFloat(Double(a[4])!), y0 = CGFloat(Double(a[5])!), x1 = CGFloat(Double(a[6])!), y1 = CGFloat(Double(a[7])!)
let w = Int((x1-x0)*s), h = Int((y1-y0)*s)
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
let ctx = NSGraphicsContext.current!.cgContext
ctx.setFillColor(CGColor(red:1,green:1,blue:1,alpha:1)); ctx.fill(CGRect(x:0,y:0,width:w,height:h))
ctx.scaleBy(x: s, y: s)
ctx.translateBy(x: -x0, y: -(b.height - y1))
p.draw(with: .mediaBox, to: ctx)
NSGraphicsContext.restoreGraphicsState()
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[8]))
