import React from 'react';

import { Form, Checkbox, Header, Radio, TextArea } from 'semantic-ui-react';

const QuestionField = ({ question, type, value, onChange }) => {
  switch (type) {
    case 'checkbox':
      return (
        <Form.Field width={12}>
          <Checkbox 
            checked={value === 'yes' ? true : false}
            label={question}
            onChange={e => onChange(question, value === 'yes' ? 'no' : 'yes')}
          />
        </Form.Field>
      );

    case 'text':
      return (
        <Form.Input
          label={question}
          value={value}
          onChange={(e, { value }) => onChange(question, value)}
        />
      );

    case 'select':
      return (
        <div className='radio-field'>
          <Header size='small'>{question.question}</Header>
          <Form.Group className='radio-group'>
            {question.options.map(option => (
              <Form.Field>
                <Radio
                  label={option}
                  value={option}
                  checked={value === option}
                  onChange={(e, { value }) => onChange(question.question, option)}
                />
              </Form.Field>
            ))}
          </Form.Group>
        </div>
      );

    case 'textfield':
      return (
        <Form.Field
          control={TextArea}
          label={question}
          value={value}
          onChange={(e, { value }) => onChange(question, value)}
        />
      );

    default:
      return null;
  }
};

export default QuestionField;
