import React, { Component } from "react";
import Emoji from "react-emoji-render";

class UserRow extends Component {
  render() {
    return (
      <tr>
        <td>{this.props.user.username}</td>
        <td>{this.props.user.followers}</td>
        <td>{this.props.user.followings}</td>
        <td>
          <Emoji text={this.props.user.full_name}></Emoji>
        </td>
        <td>{String(this.props.user.is_private)}</td>
        <td>{String(this.props.user.is_verified)}</td>
      </tr>
    );
  }
}

export default UserRow;
