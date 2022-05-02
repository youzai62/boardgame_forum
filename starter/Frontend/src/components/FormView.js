import React, { Component } from 'react';
import $ from 'jquery';
import '../css/FormView.css';

class FormView extends Component {
  constructor(props){
    super(props);
    this.access_token = ""
    this.state = {
      subject: "",
      content: "",
      token: ""
    };
  }
  submitPost = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/posts', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      headers: {
        "Authorization": "Bearer " + sessionStorage.getItem("token")
      },
      data: JSON.stringify({
        subject: this.state.subject,
        content: this.state.content
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.props.history.push('/posts')
      },
      error: (error) => {
        alert('Unable to create post. Please try your request again')
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
    return (
      <div id="add-form">
        <h2>Create A New Post</h2>
        <form className="form-view" id="create-post-form" onSubmit={this.submitPost}>
          <label><br></br>Subject:<br></br></label>
          <input type="text" name="subject" onChange={this.handleChange}/>
          <label><br></br>Summary:<br></br></label>
          <textarea rows='10' name="content" onChange={this.handleChange}/>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;