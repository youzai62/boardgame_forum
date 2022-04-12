import React, { Component } from 'react';
import Replyline from './Replyline';
import $ from 'jquery';
import '../css/Post.css';

class Post extends Component {
    constructor(props){
      super(props);
      this.state = {
        post_id: 0,
        subject:'',
        content:'',
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
        this.setState({page: num}, () => this.getPost());
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

    render() {
        return (
          <div className="post-view">
            <div className="posts-list">
              <h2>{this.state.subject}</h2>
              <div className="Post-holder">
                <h4>{this.state.content}</h4>
              </div>
              {this.state.replies.map((r, ind) => (
                <Replyline
                  key={r.id}
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