import React, { Component } from 'react';
import Replyline from './Replyline';
import $ from 'jquery';
import '../css/Post.css';
import { Link } from 'react-router-dom';


class Post extends Component {
    constructor(props){
      super(props);
      this.state = {
        post_id: 0,
        subject:'',
        content:'',
        reply_content:'',
        replies: [],
        page: 1,
        totalReplies: 0
      }
    }

    componentDidMount() {
      const { id } = this.props.match.params
      this.getPost(id);
    }

    getPost = (id) => {
        $.ajax({
          url: `/posts/${id}?page=${this.state.page}`, //TODO: update request URL
          type: "GET",
          success: (result) => {
            this.setState({
              post_id: result.post_id,
              subject: result.subject,
              content: result.content,
              replies: result.replies,
              totalReplies: result.total_replies
            })
          },
          error: (error) => {
            alert('Unable to load posts. Please try your request again')
          }
        })
    }

    //Select speicific page
    selectPage(num) {
        this.setState({page: num}, () => this.getPost(this.state.post_id));
    }

    createPagination(){
        let pageNumbers = [];
        let maxPage = Math.ceil(this.state.totalReplies / 5)
        for (let i = 1; i <= maxPage; i++) {
          pageNumbers.push(
            <span
              key={i}
              className={`page-num ${i === this.state.page ? 'active' : ''}`}
              onClick={() => {this.selectPage(i)}}>{i}
            </span>)
        }
        return pageNumbers;
    }

    //Delete a specific reply
    deleteAction = (id) => (action) => {
      if(action === 'DELETE') {
        if(window.confirm('are you sure you want to delete the reply?')) {
          $.ajax({
            url: `/replies/${id}`, //TODO: update request URL
            type: "DELETE",
            headers: {
              "Authorization": "Bearer " + sessionStorage.getItem("token")
            },
            success: (result) => {
              this.componentDidMount();
            },
            error: (error) => {
              alert('Unable to load post. Please try your request again')
            }
          })
        }
      }
    }

    submitReply = (id) => (event) => {
      event.preventDefault();
      $.ajax({
        url: `/posts/${id}`, //TODO: update request URL
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        headers: {
          "Authorization": "Bearer " + sessionStorage.getItem("token")
        },
        data: JSON.stringify({
          content: this.state.reply_content
        }),
        xhrFields: {
          withCredentials: true
        },
        crossDomain: true,
        success: (result) => {
          window.location.reload()
        },
        error: (error) => {
          alert('Unable to create reply. Please try your request again')
        }
      })
    }

    handleChange = (event) => {
      this.setState({[event.target.name]: event.target.value})
    }

    render() {
        return (
          <div className="post-view">
            <div className="posts-list">
              <h2>{this.state.subject}</h2>
              <div className="Post-holder">
                <h4>{this.state.content}</h4>
              </div>
              <Link className="Post" to={`/editpost/${this.state.post_id}`}>Update</Link>
              <form className="reply-view" id="create-reply-form" onSubmit={this.submitReply(this.state.post_id)}>
                <label><br></br>Reply:<br></br></label>
                <textarea rows='10' name="reply_content" onChange={this.handleChange}/>
                <input type="submit" className="button" value="Submit" />
              </form>
              {this.state.replies.map((r, ind) => (
                <Replyline
                  key={r.id}
                  id={r.id}
                  subject={r.content}
                  deleteAction={this.deleteAction(r.id)}
                />
              ))}
              <div className="pagination-menu">
                {this.createPagination()}
              </div>
            </div> 
          </div>
        );
    }
}

export default Post;