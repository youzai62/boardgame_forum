import React, { Component } from 'react';
import $ from 'jquery';
import '../css/FormView.css';

class UpdateForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            post_id: 0,
            subject: "",
            content: ""
        };
    }

    componentDidMount() {
        const { id } = this.props.match.params;
        this.getPost(id);
    }

    getPost = (id) => {
        $.ajax({
            url: `/posts/${id}`, //TODO: update request URL
            type: "GET",
            success: (result) => {
                this.setState({
                    post_id: result.post_id,
                    subject: result.subject,
                    content: result.content
                })
            },
            error: (error) => {
                alert('Unable to load posts. Please try your request again')
            }
        })
    }

    updatePost = (event) => {
        event.preventDefault();
        $.ajax({
            url: `/posts/${this.state.post_id}`, //TODO: update request URL
            type: "PATCH",
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
                this.props.history.push(`/posts/${this.state.post_id}`)
            },
            error: (error) => {
                alert('Unable to create post. Please try your request again')
            }
        })
    }

    handleChange = (event) => {
        this.setState({ [event.target.name]: event.target.value })
    }

    render() {
        return (
            <div id="add-form">
                <h2>Update the Post</h2>
                <form className="form-view" id="create-post-form" onSubmit={this.updatePost}>
                    <label><br></br>Subject:<br></br></label>
                    <input type="text" name="subject" placeholder={this.state.subject} onChange={this.handleChange} />
                    <label><br></br>Summary:<br></br></label>
                    <textarea rows='10' name="content" placeholder={this.state.content} onChange={this.handleChange} />
                    <input type="submit" className="button" value="Update" />
                </form>
            </div>
        );
    }
}

export default UpdateForm;