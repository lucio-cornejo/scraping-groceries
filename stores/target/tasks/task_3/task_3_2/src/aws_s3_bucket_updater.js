require('dotenv').config();

const { S3 } = require('aws-sdk');

// Configure the AWS region
const s3 = new S3({
  region: process.env.AWS_REGION,
  accessKeyId: process.env.ACCESS_KEY_ID,
  secretAccessKey: process.env.ACCESS_KEY_SECRET
});

// Function to upload JSON to S3
const uploadJsonToS3 = async (bucketName, keyName, jsonData) => {
  const params = {
    Bucket: bucketName,
    Key: keyName,
    Body: JSON.stringify(jsonData, null, 4),
    ContentType: 'application/json'
  };

  try {
    const data = await s3.upload(params).promise();
    console.log(`File uploaded successfully. ${data.Location}`);
  } catch (error) {
    console.error('Error uploading file:', error);
  }
};

const downloadJsonInS3 = async (bucketName, keyName) => {
  const params = {
    Bucket: bucketName,
    Key: keyName
  }

  const data = await s3.getObject(params).promise();
  return data.Body.toString('utf-8');
}


module.exports = {
  downloadJsonInS3: downloadJsonInS3,
  uploadJsonToS3: uploadJsonToS3
}
