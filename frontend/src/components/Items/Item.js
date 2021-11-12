import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import Badge from "react-bootstrap/Badge";
import Row from "react-bootstrap/Row";
import Skeleton from "react-loading-skeleton";
import Container from "react-bootstrap/Container";
const Item = ({ item }) => {
    // const {
    //     _id,
    //     available,
    //     category,
    //     description,
    //     isFlagged,
    //     name,
    //     photos,
    //     price,
    //     sellerID,
    //     watchlist,
    // } = item;

    return (
        <Col>
            <Card>
                {item ? (
                    <Card.Img variant="top" src={`https://picsum.photos/378/160?${item?._id}`} />
                ) : (
                    <Container>
                        <Skeleton width="100%" height={160} />
                    </Container>
                )}
                <Card.Body>
                    <Card.Title>{item?.name || <Skeleton />}</Card.Title>
                    <Card.Text>{item?.description || <Skeleton />}</Card.Text>
                    <div style={{ display: "flex" }}>
                        <Card.Text style={{ display: "inline", flex: 1 }}>
                            {item?.price ? `${item?.price}` : <Skeleton />}
                        </Card.Text>
                        {item && <Button>Buy Now</Button>}
                    </div>
                </Card.Body>
                <Card.Footer>
                    {item?.category ? (
                        item?.category.map((c, i) => (
                            <Col md="auto">
                                <Badge key={i}>{c}</Badge>
                            </Col>
                        ))
                    ) : (
                        <Skeleton />
                    )}
                    <Row></Row>
                </Card.Footer>
            </Card>
        </Col>
    );
};

export default Item;
