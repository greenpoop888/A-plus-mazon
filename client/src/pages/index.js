import React, { useState } from 'react';
import { Container, Header, Label, Segment, Grid } from 'semantic-ui-react';
import Categories from '../components/category_button';
import Items from '../components/items';
import Stories from '../components/store_selection';

const Home = () => {
    const [store, setStore] = useState('');
    const [selectedCategories, setSelectedCategories] = useState({
        primary: '',
        secondary: '',
        tertiary: ''
    });

    const handleStoreChange = (store) => {
        setStore(store);
    }

    const handleCategoryChange = (categories) => {
        setSelectedCategories(categories);
    };

    return (
        <Container>
            <Segment>
                <Grid>
                    <Grid.Row>
                        <Grid.Column computer={4} tablet={5} mobile={16}>
                            <Header as='h1' style={{ margin: 0 }}>
                                <Label size='massive' color='orange'>A+mazon⟷</Label>
                            </Header>
                        </Grid.Column>
                        <Grid.Column computer={4} tablet={11} mobile={16} floated='right'>
                            <Stories store={store} onStoreChange={handleStoreChange} />
                        </Grid.Column>
                    </Grid.Row>
                    <Grid.Row verticalAlign='middle'>
                        <Grid.Column computer={16} tablet={16} mobile={16}>
                            <Categories onCategoryChange={handleCategoryChange} />
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Segment>
            <Items
                store={store}
                primaryCategory={selectedCategories.primary}
                secondaryCategory={selectedCategories.secondary}
                tertiaryCategory={selectedCategories.tertiary}
            />
        </Container>
    );
};

export default Home;