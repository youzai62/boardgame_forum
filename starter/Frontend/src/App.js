import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

// import logo from './logo.svg';
import './css/App.css';
import FormView from './components/FormView';
import PostsView from './components/PostsView';
import Header from './components/Header.js';
import Post from './components/Post.js';


class App extends Component {
  render() {
    return (
    <div className="App">
      <Header path />
      <Router>
        <Switch>
          <Route path="/" exact component={PostsView} />
          <Route path="/createpost" component={FormView} />
          <Route path="/posts/:id" component={Post} />
          <Route component={PostsView} />
        </Switch>
      </Router>
    </div>
  );

  }
}

export default App;