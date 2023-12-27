const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const Cloudant = require('@cloudant/cloudant');

// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: '2RSbEQEdKauPD-2w-cFHObUEXiY-nlL1dh-K73I-LhwA' } }, // Replace with your IAM API key
            url: 'https://7a840525-a6d4-4a03-bf5c-2c4a4c6426af-bluemix.cloudantnosqldb.appdomain.cloud/', // Replace with your Cloudant URL
        });

        const db = cloudant.use('dealerships');
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

app.get('/api/dealership',(req,res)=>{
    const state = req.query.state;
    const selector = {};
    if (state) {
        selector.state = state;
    }else{
        return res.status(404).json({error: 'The state does not exist'});
    }

    const queryOptions = {
        selector
    };

    db.find(queryOptions,(err,body)=>{
        if(err){
            return res.status(500).json({error:'Something went wrong on the server'})
        }else{
            //console.log(body.docs);
            const dealerships =  body.docs;
            if(dealerships.length == 0){
                return res.status(404).json({error: 'Database is empty'});
            }
            return res.json(dealerships);
        }
        
    })
})

// Define a route to get all dealerships with optional state and ID filters
app.get('/dealerships/get', (req, res) => {
    const { state, id } = req.query;

    // Create a selector object based on query parameters
    const selector = {};
    if (state) {
        selector.state = state;
    }
    
    if (id) {
        selector.id = parseInt(id); // Filter by "id" with a value of 1
    }

    const queryOptions = {
        selector,
        limit: 10, // Limit the number of documents returned to 10
    };

    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching dealerships:', err);
            res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
        } else {
            const dealerships = body.docs;
            res.json(dealerships);
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});