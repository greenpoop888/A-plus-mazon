import React from 'react';
import { Container, Header, Label, Segment } from 'semantic-ui-react';
import DropdownExampleSearchSelectionTwo from '../components/category_button';
import Items from '../components/items';

const Home = () => {
    return (
        <Container>
            <Header as='h1'><Label size='massive' color='orange'>A+mazon⟷</Label></Header>
            <Segment>
                <DropdownExampleSearchSelectionTwo />
            </Segment>
            <Items />
        </Container>
    );
};

export default Home;