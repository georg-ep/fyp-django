const fs = require("fs");

function readFile(filePath) {
  let fileData;
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) throw err;
    fileData = data;
  });
  return fileData;
}

const express = require('express');
const bodyParser = require('body-parser');

const app = express();

const users = [
  {id: 1, name: "George"},
  {id: 2, name: "James"},
];

app.use(bodyParser.json());

app.get("/users/:id", (req, res) => {
  const id = parseInt(req.params.id);
  const user = users.find(user => user.id === id);
  if (!user) {
    res.status(404).send("User not found");
  } else {
    res.send(user);
  }
});