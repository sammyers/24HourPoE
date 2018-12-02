import React from 'react';
import { Form, Header, Grid } from 'semantic-ui-react';

import QuestionField from './QuestionField';

const Questions = ({ groups, values, onChange }) => {
  return (
    <Form>
      {groups.map(({ name, label, type, questions }) => (
        <div className='question-group'>
          <Header size='medium'>{label}</Header>
          <Form.Group key={name} className='question-list'>
            <Grid columns={Math.min(questions.length, 3)}>
              {questions.map(question => (
                <Grid.Column key={question.question || question}>
                  <QuestionField
                    question={question}
                    type={type}
                    value={values[name][question.question || question]}
                    onChange={(question, value) => onChange(name, question, value)}
                  />
                </Grid.Column>
              ))}
            </Grid>
          </Form.Group>
        </div>
      ))}
    </Form>
  );
};

export default Questions;
