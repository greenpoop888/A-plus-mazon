import React, { useState } from 'react';
import { Container, Header, Label, Segment, Grid } from 'semantic-ui-react';
import Categories from '../components/category_button';
import Items from '../components/items';

const Home = () => {
    const [selectedCategories, setSelectedCategories] = useState({
        primary: '',
        secondary: '',
        tertiary: ''
    });

    const handleCategoryChange = (categories) => {
        setSelectedCategories(categories);
    };

    return (
        <Container>
            <Segment>
                <Grid>
                    <Grid.Row verticalAlign='middle'>
                        <Grid.Column computer={4} tablet={5} mobile={16}>
                            <Header as='h1' style={{ margin: 0 }}>
                                <Label size='massive' color='orange'>A+mazon⟷</Label>
                            </Header>
                        </Grid.Column>
                        <Grid.Column computer={12} tablet={11} mobile={16}>
                            <Categories onCategoryChange={handleCategoryChange} />
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Segment>
            <Items
                primaryCategory={selectedCategories.primary}
                secondaryCategory={selectedCategories.secondary}
                tertiaryCategory={selectedCategories.tertiary}
            />
        </Container>
    );
};

export default Home;