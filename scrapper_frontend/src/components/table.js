import React, { Component } from "react";
import axios from "axios";
import UserRow from "./row";

class UserTable extends Component {
  interval = null;
  state = {
    task_id: "",
    hashtag: "",
    progress: {
      progress: {
        percent: "Not yet started.",
      },
    },
    users: [],
  };

  submit = (e) => {
    e.preventDefault();
    const tag = {
      hashtag: this.state.hashtag,
    };
    let id = "";
    axios
      .post("http://127.0.0.1:8000/api/hashtag/", tag)
      .then((res) => {
        this.setState({ task_id: res.data.task_id });
        id = res.data.task_id;
        console.log(id);
      })
      .catch((err) => console.log(err));
    // var progressUrl = `http://127.0.0.1:8000/celery-progress/${task_id}`;
    this.interval = setInterval(this.getProgress, 5000);
    // CeleryProgressBar.initProgressBar(progressUrl);
  };

  getProgress = () => {
    var url = `http://127.0.0.1:8000/celery-progress/${this.state.task_id}`;
    axios
      .get(url)
      .then((res) => {
        console.log(res);
        if (res.data.success === false) {
          this.setState((prevState) => {
            let temp = Object.assign({}, prevState.progress);
            temp.progress.percent = "Task Failed";
            return { temp };
          });
          clearInterval(this.interval);
        } else if (res.data.success) {
          this.setState((prevState) => {
            let temp = Object.assign({}, prevState.progress);
            temp.progress.percent = "Task Completed";
            return { temp };
          });
          clearInterval(this.interval);
        } else {
          res.data.progress.percent = res.data.progress.percent + " %";
          this.setState({ progress: res.data });
          this.getData();
        }
      })
      .catch((err) => {
        console.log(err);
        clearInterval(this.interval);
      });
  };

  getData = () => {
    axios
      .get(`http://127.0.0.1:8000/api/hashtag/${this.state.hashtag}`)
      .then((res) => this.setState({ users: res.data }))
      .catch((err) => console.log(err));
  };
  onChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  render() {
    return (
      <React.Fragment>
        <div className="">
          <form className="mt-5 text-center w-25 p-3" onSubmit={this.submit}>
            <div className="form-group">
              <label className="form-label">Hashtag (wihtout #):</label>
              <input
                className="form-control"
                type="text"
                name="hashtag"
                onChange={this.onChange}
                value={this.state.hashtag}
              />
            </div>
            <div className="form-group">
              <button className="btn btn-info float-end" type="submit">
                Search
              </button>
            </div>
          </form>
          <div className="p-4 mt-4">
            <h6>Progress: {this.state.progress.progress.percent}</h6>
          </div>
          <div className="p-2">
            <button onClick={this.getData} className="btn btn-primary p-2">
              Fetch From Database
            </button>
          </div>
          <table className="table table-Light">
            <thead>
              <tr>
                <th>Username</th>
                <th>Followers</th>
                <th>Followings</th>
                <th>Full Name</th>
                <th>Private</th>
                <th>Verified</th>
              </tr>
            </thead>
            <tbody>
              {this.state.users.map((user) => (
                <UserRow user={user} key={user.username} />
              ))}
            </tbody>
          </table>
        </div>
      </React.Fragment>
    );
  }
}

export default UserTable;
