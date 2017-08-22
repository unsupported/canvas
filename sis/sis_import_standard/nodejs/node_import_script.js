/*Upload a CSV file to your Canvas instance with archiving*/
//Working as of 7/25/2017
//dependencies for import
const req = require('request');
const FormData = require('form-data');
const fs = require('fs');
const csv = require('fast-csv');

///////////////Edit These Variables///////////////

const importFile = '/full/path/to/file/filename.zip'; //include full path to csv or zip file
const subdomain = 'sample'; //i.e. sample.instructure.com would be 'sample'
const apiToken = ''; //
const env = 'test'; //leave null for production. For test use 'test', For beta use 'beta'
//The archive_folder needs to be a string that ends with a slash
const archive_folder = '/full/path/to/archive/folder'; //include full path to archive folder

//////////////////////////////////////////////////
let formData = {
  attachment: fs.createReadStream(importFile)
};

let fullUrl;
let dateForFile = new Date();
let importId;

const readFileForArchive = new Promise((resolve, reject) =>{
  let returnArray = [];
  fs.createReadStream(importFile)
    .pipe(csv())
    .on('data', function(data) {
      returnArray.push(data);
    })
    .on('end', function(data) {
      // console.log('Read finished');
      if (returnArray.length > 0) {
        resolve(returnArray);
      } else {
        reject(Error("Error! CSV Read Failed!"));
      }
    });
});

// const deleteUploadFile = (cb)=>{
//   fs.unlink(importFile, cb);
// };

const archiveFile = ()=>{
  if(importFile.indexOf('.csv') > -1){
    fs.rename(importFile, archive_folder + importId + '.csv', (err)=>{
      if(err) console.log(`Error: ${err}`);
    });
  } else if (importFile.indexOf('.zip') > -1) {
    fs.rename(importFile, archive_folder + importId + '.zip', (err)=>{
      if(err) console.log(`Error: ${err}`);
    });
  } else {
    console.log('Check your file extension. Archive Failed!');
  }
};

if(env == null){
  fullUrl = `https://${subdomain}.instructure.com/api/v1/accounts/self/sis_imports`;
} else {
  fullUrl = `https://${subdomain}.${env}.instructure.com/api/v1/accounts/self/sis_imports`;
}
console.log(`Posting to ${fullUrl}`);
req.post(fullUrl, {
  'auth': {
    'bearer': apiToken
  }, formData: formData
}, (err, response, body) => {
  if (err) {
    return console.error('upload failed:', err);
  }
  importId = `import_id_${JSON.parse(body).id}`;
  console.log(importId);
  console.log('Upload successful!  Server responded with: ', body);
  readFileForArchive.then(archiveFile()).catch((e) => {
    console.log(`Error: ${e}`);
  });
});
