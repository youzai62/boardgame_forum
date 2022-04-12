import React, { Component } from 'react';
import '../css/Post.css';


class Replyline extends Component {
  constructor(props){
    super(props);
    this.state = {
      deletable: false
    }
  }

  flipVisibility() {
    this.setState({deletable: !this.state.deletable});
  }

  render() {
    const {subject} = this.props;
    return (
      <div className="Reply-holder">
        <div className="Reply">{subject}</div>
        <div className="Post-status">
            <img style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}} src="delete.png" className="delete" onClick={() => this.props.deleteAction('DELETE')}/>
        </div>
      </div>
    );
  }
}

export default Replyline;