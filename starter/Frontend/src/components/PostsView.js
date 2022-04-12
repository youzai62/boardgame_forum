import React, { Component } from 'react';
import '../css/App.css';
import Postline from './Postline';
import Search from './Search';
import $ from 'jquery';

class PostsView extends Component {
  constructor(props){
    super(props);
    this.state = {
      posts: [],
      page: 1,
      totalPosts: 0
    }
  }

  componentDidMount() {
    this.getPosts();
  }

  //Get all posts
  getPosts = () => {
    $.ajax({
      url: `/posts?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          posts: result.posts,
          totalPosts: result.total_posts,
        })
      },
      error: (error) => {
        alert('Unable to load posts. Please try your request again')
      }
    })
  }

  //Select speicific page
  selectPage(num) {
    this.setState({page: num}, () => this.getPosts());
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalPosts / 15)
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

  //Search Post
  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/posts/result`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          posts: result.posts,
          totalPosts: result.total_posts
        })
      },
      error: (error) => {
        alert('Unable to load posts. Please try your request again')
      }
    })
  }

  //Retrive specific post
  getAction = (id) =>  (action) => {
    if(action === 'GET') {
      $.ajax({
        url: `/posts/${id}`, //TODO: update request URL
        type: "GET",
        success: (result) => {
          this.getPosts();
        },
        error: (error) => {
          alert('Unable to load posts. Please try your request again')
        }
      })
    }
  }

  //Delete a specific post
  deleteAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the post?')) {
        $.ajax({
          url: `/posts/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getPosts();
          },
          error: (error) => {
            alert('Unable to load posts. Please try your request again')
          }
        })
      }
    }
  }

  render() {
    return (
      <div className="posts-view">
        <div className="search bar">
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="posts-list">
          <h2>Posts</h2>
          {this.state.posts.map((p, ind) => (
            <Postline
              id={p.id}
              subject={p.subject}
              getAction={this.getAction(p.id)}
              deleteAction={this.deleteAction(p.id)}
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

export default PostsView;