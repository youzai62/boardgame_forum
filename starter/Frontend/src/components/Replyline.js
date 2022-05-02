import React, { Component } from 'react';
import '../css/Post.css';


class Replyline extends Component {

  render() {
    const {subject} = this.props;
    return (
      <div className="Reply-holder">
        <div className="Reply">{subject}</div>
        <div className="Post-status">
          <img alt="deleted" src="../delete.png" className="delete" onClick={() => this.props.deleteAction('DELETE')}/>
        </div>
      </div>
    );
  }
}

export default Replyline;