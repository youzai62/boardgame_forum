import React, { Component } from 'react';
import logo from '../logo.svg';
import '../css/Header.css';

class Header extends Component {

    navTo(uri){
      window.location.href = window.location.origin + uri;
    }
  
    render() {
      return (
        <div className="App-header">
          <h1 onClick={() => {this.navTo('')}}>Boardgame Forum</h1>
          <h2 onClick={() => {this.navTo('/login')}}>login</h2>
        </div>
      );
    }
  }
  
  export default Header;