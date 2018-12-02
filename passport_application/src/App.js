import React, { Component } from 'react';
import { Header, Button, Icon } from 'semantic-ui-react';

import Questions from './Questions';

import './App.css';

class App extends Component {
  state = {
    phase: 'loading',
    groups: [],
    responses: {},
  };

  async componentDidMount() {
    const response = await fetch('/questions');
    const { groups } = await response.json();
    this.setState({
      phase: 'loaded',
      groups,
      responses: this.getBlankResponses(groups),
    });
  }

  getBlankResponses = groups => {
    return groups.reduce((all, { name, questions, type }) => ({
      ...all,
      [name]: questions.reduce((all, question) => ({
        ...all,
        [question.question || question]: type === 'checkbox' ? 'no' : '',
      }), {}),
    }), {});
  };

  handleChange = (group, name, value) => {
    this.setState({
      responses: {
        ...this.state.responses,
        [group]: {
          ...this.state.responses[group],
          [name]: value,
        },
      },
    });
  };

  handleSubmit = async () => {
    const response = await fetch('/print-form', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ responses: this.state.responses }),
    });
    if (response.ok) {
      this.setState({ phase: 'submitted' });
      setTimeout(() => this.setState({
        phase: 'loaded',
         responses: this.getBlankResponses(this.state.groups),
      }), 4000);
    }
  };

  render() {
    const { phase, groups, responses } = this.state;
    let ui;
    switch (phase) {
      case 'loading':
        ui = (
          <div>
            <Header size='medium'>
              Loading...
            </Header>
          </div>
        );
        break;

      case 'loaded':
        ui = (
          <Questions
            groups={groups}
            values={responses}
            onChange={this.handleChange}
          />
        );
        break;

      case 'submitted':
        ui = (
          <div>
            <Header size='medium'>Thanks for submitting!</Header>
            <Header sub>Good luck.</Header>
          </div>
        );
        break;

      default:
        ui = null;
    }
    const loaded = phase === 'loaded';
    const valid = loaded ?
      responses.short_answer['First Name'] && responses.short_answer['Last Name']
      : false;

    return (
      <div className="App">
        <header className="App-header">
          <Header>Buffalonia Border Entry Application</Header>
          {ui}
          {phase === 'loaded' && valid &&
            <Button icon color='green' labelPosition='left' onClick={this.handleSubmit}>
              <Icon name='print' />
              Print Application
            </Button>
          }
        </header>
      </div>
    );
  }
}

export default App;
