import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom'
import './css/index.css';
import App from './App';
//import * as serviceWorker from './serviceWorker';
import Auth0ProviderWithHistory from './auth/Auth0ProviderWithHistory';

ReactDOM.render(
  <Router>
    <Auth0ProviderWithHistory>
      <App />
    </Auth0ProviderWithHistory>
  </Router>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
//serviceWorker.unregister();


 //"start": "HOST='127.0.0.1' PORT='5000' react-scripts start",