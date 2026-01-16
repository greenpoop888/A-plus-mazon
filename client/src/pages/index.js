import React, { useState } from 'react';
import { Container, Header, Label, Segment } from 'semantic-ui-react';
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
            <Header as='h1'><Label size='massive' color='orange'>A+mazon⟷</Label></Header>
            <Segment>
                <Categories onCategoryChange={handleCategoryChange} />
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