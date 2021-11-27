import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getAllItems, getCategories, resetSearchItems, searchItem } from "../../slices/items";
import ItemCard from "./ItemCard";
import ItemSkeleton from "./ItemSkeleton";
import Row from "react-bootstrap/Row";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";

const Items = () => {
    const { items, searchItems, categories } = useSelector((state) => state.items);
    const [searchTerm, setSearchTerm] = useState("");
    const [category, setCategory] = useState("");
    const [searchMode, setSearchMode] = useState(false);
    const dispatch = useDispatch();
    const formRef = useRef();
    const getItems = () => {
        dispatch(getAllItems());
    };

    const fetchCategories = () => {
        dispatch(getCategories());
    };

    useEffect(() => {
        getItems();
        fetchCategories();
    }, []);

    const handleSearch = () => {
        setSearchMode(true);
        dispatch(
            searchItem({
                keywords: searchTerm.split(" "),
                category: category.length ? category : null,
            })
        );
    };

    const clearSearch = () => {
        setSearchMode(false);
        setSearchTerm("");
        setCategory("");
        formRef.current.reset();
        dispatch(resetSearchItems());
    };

    let itemCards = items.map((item, i) => <ItemCard key={i} item={item} />);
    if (itemCards.length == 0) {
        itemCards = Array.from(Array(10))
            .fill(0)
            .map((_, i) => <ItemSkeleton key={i} />);
    }

    let searchItemCards = searchItems.map((item, i) => <ItemCard key={i} item={item} />);
    if (searchItemCards.length == 0) {
        searchItemCards = Array.from(Array(10))
            .fill(0)
            .map((_, i) => <ItemSkeleton key={i} />);
    }

    console.log("searchItems", searchItems);
    return (
        <div>
            <h1>Items</h1>
            <Form
                onSubmit={(e) => {
                    e.preventDefault();
                    handleSearch();
                }}
                ref={formRef}
            >
                <Row>
                    <Col>
                        <Form.Control
                            placeholder="search"
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </Col>

                    <Col>
                        <Form.Control
                            as="select"
                            // custom
                            onChange={(e) => setCategory(e.target.value)}
                        >
                            <option>Select a category</option>,
                            {categories.length ? (
                                categories.map((category, i) => (
                                    <option key={i} value={category}>
                                        {category}
                                    </option>
                                ))
                            ) : (
                                <option>Loading</option>
                            )}
                        </Form.Control>
                    </Col>
                    <Col>
                        <Button onClick={handleSearch}>Search</Button>{" "}
                        <Button variant="danger" onClick={clearSearch}>
                            Clear
                        </Button>
                    </Col>
                </Row>
            </Form>
            <br />
            <Row xs={1} md={3} className="g-4">
                {searchMode ? searchItemCards : itemCards}
            </Row>
        </div>
    );
};

export default Items;
