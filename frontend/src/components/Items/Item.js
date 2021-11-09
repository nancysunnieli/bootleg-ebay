import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";

const Item = ({ item }) => {
    const {
        _id,
        available,
        category,
        description,
        isFlagged,
        name,
        photos,
        price,
        sellerID,
        watchlist,
    } = item;
    return (
        <Col>
            <Card>
                <Card.Img
                    variant="top"
                    src={`https://picsum.photos/378/160?${new Date().toISOString()}`}
                />
                <Card.Body>
                    <Card.Title>{name}</Card.Title>
                    <Card.Text>{description}</Card.Text>
                    <div style={{ display: "flex" }}>
                        <Card.Text style={{ display: "inline", flex: 1 }}>${price}</Card.Text>
                        <Button>Buy Now</Button>
                    </div>
                </Card.Body>
            </Card>
        </Col>
    );
};

export default Item;
