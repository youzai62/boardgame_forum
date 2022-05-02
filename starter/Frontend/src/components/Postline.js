import React, { Component } from 'react';
import '../css/Post.css';
import { Link } from 'react-router-dom';


class Postline extends Component {
  render() {
    const { id, subject} = this.props;
    return (
      <div className="Post-holder">
        <Link className="Post" to={`/posts/${id}`}>{subject}</Link>
        <div className="Post-status">
          <img alt="deleted" src="delete.png" className="delete" onClick={() => this.props.deleteAction('DELETE')}/>
        </div>
      </div>
    );
  }
}

export default Postline;
