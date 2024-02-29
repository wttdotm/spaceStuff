const fetch = require('node-fetch')
var lstjs = require('local-sidereal-time');
// const JsVotable = require('jsvotable')
const HTMLParser = require('node-html-parser')

let lat = 40.682740
let lon = -73.987690

let dec = lat


var date = new Date(Date.now());
var lst_hours = lstjs.getLST(date, lon)
let ra = lst_hours
var lst_string = lstjs.lstString(date, lon);
console.log(lst_hours)

console.log(ra, dec)
let url = `https://simbad.u-strasbg.fr/simbad/sim-coo?output.format=HTML&Coord=${ra}+${dec}&CooFrame=FK5&CooEpoch=2000&CooEqui=2000&CooDefinedFrames=none&Radius=20&Radius.unit=arcmin&submit=submit+query&Ident=BA&NbIdent=cat&CoordList=`
// let url = 
// https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=text&query=SELECT%20TOP%2010%20MAIN_ID,RA,DEC%20FROM%20BASIC%20WHERE%20rvz_redshift%20%3E%203.3

// let url = `https://simbad.cds.unistra.fr/simbad/sim-tap/sync?output.format=HTML&request=doQuery&lang=adql&format=text&query=${encodeURIComponent(`SELECT TOP 10 MAIN_ID,RA,DEC FROM BASIC WHERE ra > ${ra - 0.1} AND ra < ${ra + 0.1} AND dec > ${dec - 0.1} AND dec < ${dec + 0.1} AND MAIN_ID LIKE 'BD%'`)})`
// let url = `https://simbad.cds.unistra.fr/simbad/sim-tap/sync?output.format=HTML&request=doQuery&lang=adql&format=text&query=${encodeURIComponent(`SELECT TOP 10 MAIN_ID,RA,DEC FROM BASIC WHERE ra > 5 AND ra < 5.5848222958047415 AND dec > 40 AND dec < 40.78274 AND MAIN_ID LIKE 'BD%'`)})`
// https://simbad.u-strasbg.fr/simbad/sim-coo?output.format=votable&Coord=${ra}+${dec}&CooFrame=FK5&CooEpoch=2000&CooEqui=2000&CooDefinedFrames=none&Radius=20&Radius.unit=arcmin&submit=submit+query&CoordList=`
// let url = `https://simbad.u-strasbg.fr/simbad/sim-coo?output.format=HTML&Coord=${ra}+${dec}&CooFrame=FK5&CooEpoch=2000&CooEqui=2000&CooDefinedFrames=none&Radius=20&Radius.unit=arcmin&submit=submit+query&CoordList=`
// let url = `http://skyserver.sdss.org/dr1/en/tools/search/x_radial.asp?ra=${encodeURI('08:35:42.03')}&dec=${encodeURI('40:40:57.864')}&radius=3&format=csv&topnum=20`
// let url = `http://skyserver.sdss.org/dr1/en/tools/search/x_radial.asp?ra=180&dec=-0.2&radius=3&format=csv&topnum=20 `
console.log(url)




let ID = ''
fetch(url)
  .then(res => res.text())
  // .then(res => {
  //   console.log("this is res")
  //   console.log(res)
  // })
  .then(res => {
    const body = HTMLParser.parse(res)
    const allLinks = body.querySelectorAll('a')
    // console.log(allLinks)
    // console.log(allLinks.length)
    //find the first href with a link to a result
    let firstResult = false
    allLinks.forEach(link => {
      // console.log(link)
      if (link?.rawAttrs && link.childNodes[0]?._rawText !== undefined) {
        // console.log("HIT THISSSSSSS")
        // console.log(link.rawAttrs)
        if (link.rawAttrs.indexOf('simbad.cds.unistra.fr/simbad/sim-id?') > -1 && !firstResult > -1) {
          console.log("HIT")
          firstResult = true
          firstResult = link.childNodes[0]._rawText
          // console.log(link)
        }
        // console.log(link.childNodes[0]?._rawText)
      }
      // if (link.rawAttrs.find("simbad.cds.unistra.fr/simbad/sim-id?") && !firstResult) {
      //   firstResult = link.rawAttributes
      // }
    })
    ID = firstResult
    console.log(firstResult)
    while (firstResult.indexOf('  ') > -1) {
      firstResult = firstResult.replace('  ', ' ')
    }
    console.log(firstResult)
    // // return firstResult


    allTrLats = body.querySelectorAll("td.lat")
    allTrLons = body.querySelectorAll("td.lon")
    // allTr.forEach(tr => {
    //   console.log(tr)
    // })
    let searchingRa = false
    let raIndex = 0
    while (!searchingRa) {
      if (allTrLats[0].childNodes[0]._rawText.length > 14) {
        searchingRa = allTrLats[0].childNodes[0]._rawText
      }
      raIndex++
    }

    let searchingDec = false
    let decIndex = 0
    while (!searchingDec) {
      if (allTrLons[0].childNodes[0]._rawText.length > 14) {
        searchingDec = allTrLons[0].childNodes[0]._rawText
      }
      decIndex++
    }

    console.log(allTrLats[0].childNodes[0]._rawText)
    console.log(allTrLons[0].childNodes[0]._rawText)
    let ra = searchingRa.replace(' ', '+')
    let dec = searchingDec.replace(' ', '+')

    return {ra, dec, ID}
    //get the text 

    //simbad.cds.unistra.fr/simbad/sim-id?
    // console.log(body.querySelector('tr'))
  })
  .then(result => {
    urlWeWant = `https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl?Position=${encodeURI(result.ra)}%2C${encodeURI(result.dec)}&survey=DSS&coordinates=J2000&coordinates=&projection=Tan&pixels=300&size=&float=on&scaling=Log&resolver=SIMBAD-NED&Sampler=_skip_&Deedger=_skip_&rotation=&Smooth=&lut=Grays&PlotColor=&grid=_skip_&gridlabels=1&catalogurl=&CatalogIDs=on&survey=_skip_&survey=_skip_&survey=_skip_&IOSmooth=&contour=&contourSmooth=&ebins=null`
    console.log(urlWeWant)
    fetch(urlWeWant)
      .then(res => res.text())
      .then(res => {
        const body = HTMLParser.parse(res)
        const image = body.querySelectorAll('img')[1]
        let srcIndex = image.rawAttrs.indexOf('src="')
        let onClickIndex = image.rawAttrs.indexOf('onclick')
        console.log(srcIndex)
        console.log(onClickIndex)
        let relativeURL = image.rawAttrs.slice(srcIndex+11,onClickIndex-10)
        // console.log(image.rawAttrs.slice(srcIndex+11,onClickIndex-10))
        let imageURL = `https://skyview.gsfc.nasa.gov/${relativeURL}`
        //https://skyview.gsfc.nasa.gov/tempspace/fits/skv9700614996176.jpg
        console.log(imageURL)
      })
  })

console.log("initial, ", ID)
// const {Observer, EquatorialToHorizontal, SiderealTime} = require('astronomy-engine')
// // import { Observer, EquatorialToHorizontal, SiderealTime } from 'astronomy-engine';

// // Define your geographic location
// const observer = new Observer(lat, lon, 0);

// // Calculate local sidereal time for the observer
// const lst = SiderealTime(new Date());
// console.log(lst)