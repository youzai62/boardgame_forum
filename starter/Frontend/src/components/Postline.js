import React, { Component } from 'react';
import '../css/Post.css';
import { Link } from 'react-router-dom';


class Postline extends Component {
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
    const { id, subject} = this.props;
    return (
      <div className="Post-holder">
        <Link className="Post" to={`/posts/${id}`}>{subject}</Link>
        <div className="Post-status">
            <img style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}} src="delete.png" className="delete" onClick={() => this.props.deleteAction('DELETE')}/>
        </div>
      </div>
    );
  }
}

export default Postline;
