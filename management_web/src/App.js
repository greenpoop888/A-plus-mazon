import 'semantic-ui-css/semantic.min.css';
import Home from './pages/index';
import { Amplify } from 'aws-amplify';
import { Authenticator, View, Heading, useTheme, ThemeProvider } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { Header, Label, Button } from 'semantic-ui-react';

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: process.env.REACT_APP_USER_POOL_ID,
      userPoolClientId: process.env.REACT_APP_CLIENT_ID,
      loginWith: {
        email: true
      }
    }
  }
});

const theme = {
  name: 'custom-theme',
  tokens: {
    colors: {
      brand: {
        primary: {
          10: { value: '#fff3e0' },
          80: { value: '#f39c12' },
          90: { value: '#e67e22' },
          100: { value: '#f2711c' },
        },
      },
    },
    components: {
      button: {
        primary: {
          backgroundColor: { value: '{colors.brand.primary.80}' },
          _hover: { backgroundColor: { value: '{colors.brand.primary.90}' } },
          _focus: {
            backgroundColor: { value: '{colors.brand.primary.100}' },
            boxShadow: { value: '0 0 0 2px #fff, 0 0 0 4px #f2711c' }
          },
          _active: { backgroundColor: { value: '{colors.brand.primary.100}' } },
        },
        link: {
          color: { value: '{colors.brand.primary.80}' },
          _hover: {
            color: { value: '{colors.brand.primary.90}' },
            backgroundColor: { value: 'transparent' }
          },
          _focus: {
            color: { value: '{colors.brand.primary.100}' },
            backgroundColor: { value: 'transparent' },
            boxShadow: { value: 'none' }
          },
          _active: {
            color: { value: '{colors.brand.primary.100}' },
            backgroundColor: { value: 'transparent' }
          }
        },
      },
      fieldcontrol: {
        _focus: {
          boxShadow: { value: '0 0 0 1px #f2711c' },
          borderColor: { value: '#f2711c' },
        },
      },
      tabs: {
        item: {
          _active: {
            color: { value: '{colors.brand.primary.80}' },
            borderColor: { value: '{colors.brand.primary.80}' },
          },
          _hover: {
            color: { value: '{colors.brand.primary.90}' },
          },
          _focus: {
            color: { value: '{colors.brand.primary.100}' },
          },
        },
      },
    },
  },
};

const components = {
  Header() {
    const { tokens } = useTheme();
    return (
      <View textAlign="center" padding={tokens.space.medium}>
        <Header as='h1'><Label size='massive' color='orange'>A+mazon⟷</Label></Header>
        <Heading level={4}>Management Portal</Heading>
        <p style={{ fontSize: '0.9rem', color: '#666' }}>Employee Only - Authorized Access Required</p>
      </View>
    );
  },
};

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#f0f2f5'
      }}>
        <Authenticator
          loginMechanisms={['email']}
          hideSignUp={true}
          components={components}
        >
          {({ signOut, user }) => (
            <main>
              <div style={{ textAlign: 'right' }}>
                <Label>{user.signInDetails?.loginId} </Label>
                <Button color='orange' inverted size='mini' onClick={signOut}>Sign Out</Button>
              </div>
              <Home />
            </main>
          )}
        </Authenticator>
      </div>
    </ThemeProvider>
  );
}

export default App;