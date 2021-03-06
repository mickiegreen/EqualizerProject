/* eslint-disable jsx-a11y/href-no-hash */
import React from 'react';
import { Grid, Cell, Textfield, Button } from '../../../../node_modules/react-mdl';
import '../../../../node_modules/react-mdl/extra/material.css';
import '../../../../node_modules/react-mdl/extra/material.js';
import Page from '../../../components/Page/Page';
import RequireAuth from '../Auth';
import styles from './Profile.scss';
import { getUserName } from '../jwtUtils';


class Profile extends React.Component {

  constructor(props) {
    super(props);
    //const { user } = this.props.user;
    //const { email } = this.props.user;
      //const { user } = getUserName();
      //const { email } = getUserName();
      const { user } = 'Michael';
      const { email } = 'michael.green@gmail.com';
    this.state = {
      email,
      password: '',
    };
    if (localStorage.getItem('jwtToken') === null || localStorage.getItem('jwtToken') === undefined ){
      window.location.replace('/');
    }
  }

  handlePasswordChange = (e) => {
    this.setState({ password: e.target.value });
  }

  handleEmailChange = (e) => {
    const value = e.target.value;

    this.setState({ email: value });
  }

  render() {
    const { email, street, state, zip } = this.state;
    return (
      <Page heading='Profile' >
        <div >
          <Grid>
            <form style={{ width: '100%', margin: 'auto' }} >

              <Cell col={12} >
                <Textfield onChange={this.handleEmailChange.bind(this)} label='Email' value={email} floatingLabel />
              </Cell>

              <Cell col={12} style={{ textAlign: 'right' }} >
                <Button primary >Sign up</Button>

              </Cell>

              <hr />
              <h2 className={styles.heading} >
                Default Address
              </h2>


              <Cell col={12} >
                <Textfield
                  onChange={this.handleEmailChange.bind(this)} label='Street' value={street}
                  floatingLabel
                />
              </Cell>
              <Cell col={12} >
                <Textfield
                  onChange={this.handleEmailChange.bind(this)} label='State' value={state}
                  floatingLabel
                />
              </Cell>
              <Cell col={12} >
                <Textfield
                  onChange={this.handleEmailChange.bind(this)} label='Zip Code' value={zip}
                  floatingLabel
                />
              </Cell>

              <Cell col={12} style={{ textAlign: 'right' }} >
                <Button primary >Sign up</Button>

              </Cell>
            </form>


          </Grid>


        </div>

      </Page>
    )
      ;
  }


}

export default Profile;
