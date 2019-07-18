import React from 'react';

import Amplify, { API, Storage } from "aws-amplify";
import { withAuthenticator } from 'aws-amplify-react';
import awsmobile from "./aws-exports";

import logo from './logo.svg';
import './App.css';

Amplify.configure(awsmobile);

API.configure({
  endpoints: [
    {
      name: "ApiGatewayRestApi",
      // endpoint: "https://lr6ss16qj3.execute-api.us-east-1.amazonaws.com/dev"
      endpoint: awsmobile.aws_cloud_logic_custom[0].endpoint
    }
  ]
});

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default withAuthenticator(App);
