import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import Badge from "react-bootstrap/Badge";
import Row from "react-bootstrap/Row";
import Skeleton from "react-loading-skeleton";
import Container from "react-bootstrap/Container";
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
                    // src={`data:image/png;base64, ${photos}`}
                    src={`https://picsum.photos/500?${_id}`}
                />
                <Card.Body>
                    <Card.Title>{name}</Card.Title>
                    <Card.Text>{description}</Card.Text>
                </Card.Body>
                <Card.Footer>
                    <Row>
                        {item.category.map((c, i) => (
                            <Col md="auto">
                                <Badge key={i}>{c}</Badge>
                            </Col>
                        ))}
                    </Row>
                </Card.Footer>
            </Card>
        </Col>
    );
};

export default Item;
