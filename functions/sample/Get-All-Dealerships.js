/**
 * This Cloud Function retrieves a list of dealerships with optional filtering by city and state.
 *
 * @param {object} params - A JSON object containing optional query parameters 'city' and 'state'.
 * @returns {object} - A JSON object containing a list of dealerships with details.
 */
const Cloudant = require('@cloudant/cloudant');

async function getDealerships(params) {
  try {
    // Cloudant database credentials
    const cloudantUrl = '"https://4de1e689-95a2-4931-a915-ecb3999d0311-bluemix.cloudantnosqldb.appdomain.cloud"';
    const databaseName = 'dealerships'; // Replace with your database name

    // Initialize Cloudant
    const cloudant = Cloudant({ url: cloudantUrl, plugins: 'promises' });

    // Connect to the database
    const dealershipDb = cloudant.db.use(databaseName);

    // Build the query based on parameters provided (optional)
    const query = {};
    if (params.city) query.city = params.city;
    if (params.state) query.state = params.state;

    // Query the database with the optional filter
    const result = await dealershipDb.find({
      selector: query,
      fields: ['_id', 'city', 'state', 'st', 'address', 'zip', 'lat', 'long'],
    });

    // Extract and format the data as specified
    const dealerships = result.docs.map(doc => ({
      id: doc._id,
      city: doc.city,
      state: doc.state,
      st: doc.st,
      address: doc.address,
      zip: doc.zip,
      lat: doc.lat,
      long: doc.long,
    }));

    // If no dealerships found, return a 404 error
    if (dealerships.length === 0) {
      return {
        statusCode: 404,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ error: 'No dealerships found' }),
      };
    }

    return dealerships;
  } catch (error) {
    console.error('Error:', error);
    // Handle other errors with a 500 status code
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Something went wrong on the server' }),
    };
  }
}

module.exports.main = async function(params) {
  try {
    const dealerships = await getDealerships(params);

    // If the response is an error (404 or 500), return it directly
    if (dealerships.statusCode) {
      return dealerships;
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dealerships),
    };
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Internal Server Error' }),
    };
  }
};
