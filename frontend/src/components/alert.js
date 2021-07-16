import React, { Component } from 'react';

export class Alert extends Component {

  constructor(props, context) {
    super(props, context);
    this.state = {
      isActive: true,
    }
  }

  hideAlert() {
    this.setState({
      isActive: false,
    });
  }

  render() {
    if (this.state.isActive) {
      return (
            <div class="alert alert-warning alert-dismissible fade show" role="alert">
            <strong>RobotStatus</strong> Prueba de concepto.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" onClick={() => this.hideAlert()}>
            </button>
            {this.props.text}
          </div>
      );
    }
    return <div/>
  }
}

