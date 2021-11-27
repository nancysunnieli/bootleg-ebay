import moment from "moment";
import { useEffect, useState } from "react";
import Badge from "react-bootstrap/Badge";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Image from "react-bootstrap/Image";
import ProgressBar from "react-bootstrap/ProgressBar";
import Row from "react-bootstrap/Row";
import Table from "react-bootstrap/Table";
import { useDispatch, useSelector } from "react-redux";
import { useHistory, useParams } from "react-router-dom";
import { clearItem, getCategories, getItem, removeItem } from "../../slices/items";
import Loading from "../Loading/Loading";
import NotFound from "../NotFound/NotFound";
import CreateAuctionModal from "./CreateAuctionModal";
import EditItemModal from "./EditItemModal";
import ReportModal from "./ReportItemModal";
import WatchlistModal from "./WatchlistModal";

export default function Item() {
    const { item_id } = useParams();
    const dispatch = useDispatch();
    const { user } = useSelector((state) => state.auth);
    const [showEditItemModal, setEditItemModalVisible] = useState(false);
    const [showCreateAuctionModal, setCreateAuctionModalVisible] = useState(false);
    const [watchlistModalVisible, setWatchlistModalVisible] = useState(false);
    const history = useHistory();
    const [reportModalVisible, setReportModalVisible] = useState(false);
    const { item, isGetItemLoading } = useSelector((state) => state.items);
    useEffect(() => {
        dispatch(getItem({ item_id }));
        dispatch(getCategories());

        return () => {
            dispatch(clearItem());
        };
    }, []);

    if (isGetItemLoading) {
        return <Loading />;
    }

    if (item == null) {
        return <NotFound />;
    }

    const { _id, category, description, isFlagged, name, photos, quantity, sellerID, watchlist } =
        item.item;

    let isSeller = false;
    if (sellerID == user.user_id) {
        isSeller = true;
    }

    console.log("item", item);

    const upcomingAuctions = item.auction.filter((a) => a.end_time * 1000 > new Date().getTime());
    const pastAuctions = item.auction.filter((a) => a.end_time * 1000 < new Date().getTime());
    const itemHasBids = item.auction.some((a) => a.bids.length > 0);

    const handleDelete = () => {
        dispatch(removeItem({ item_id: _id, history }));
    };

    return (
        <div>
            <Container style={{ width: "80%", marginBottom: "2rem" }}>
                <Row>
                    <Col>
                        <Image
                            src="https://picsum.photos/1000"
                            style={{
                                width: "30em",
                                height: "auto",
                                display: "block",
                            }}
                        />
                    </Col>
                    <Col>
                        <h1>{name}</h1>
                        <h4>{description}</h4>
                        <h5>Quantity: {quantity}</h5>

                        <Row>
                            {category.map((c, i) => (
                                <Col md="auto" key={i}>
                                    <Badge key={i} bg="primary">
                                        {c}
                                    </Badge>
                                </Col>
                            ))}
                        </Row>
                        <br />
                        <Row>
                            <Button variant="info" onClick={() => setWatchlistModalVisible(true)}>
                                Add Item To Watchlist
                            </Button>
                        </Row>
                        <br />
                        <Row>
                            <Button variant="warning" onClick={() => setReportModalVisible(true)}>
                                Report Item
                            </Button>
                        </Row>
                        {isSeller && (
                            <div>
                                <br />
                                <Row>
                                    <Button onClick={() => setCreateAuctionModalVisible(true)}>
                                        Create Auction
                                    </Button>
                                </Row>
                                <br />
                                <Row>
                                    <Button
                                        variant="info"
                                        onClick={() => setEditItemModalVisible(true)}
                                    >
                                        Edit Item
                                    </Button>
                                </Row>
                                <br />
                                <Row>
                                    <Button
                                        variant="danger"
                                        disabled={itemHasBids}
                                        onClick={handleDelete}
                                    >
                                        Delete Item
                                    </Button>
                                </Row>
                            </div>
                        )}
                    </Col>
                </Row>
                <br />
                <h3>Upcoming Auctions</h3>
                <Row>
                    <Table striped hover responsive="sm">
                        <thead>
                            <tr>
                                <th>Starts</th>
                                <th>Ends</th>
                                <th>View</th>
                            </tr>
                        </thead>
                        <tbody>
                            {upcomingAuctions.map((a, i) => (
                                <tr>
                                    <td>{moment(a.start_time * 1000).fromNow()}</td>
                                    <td>{moment(a.end_time * 1000).fromNow()}</td>
                                    <td>
                                        <Button
                                            size="sm"
                                            onClick={() =>
                                                history.push(`/auctions/${a.auction_id}`)
                                            }
                                        >
                                            View
                                        </Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                </Row>
                <br />
                <h3>Past Auctions</h3>
                <Row>
                    <Table striped hover responsive="sm">
                        <thead>
                            <tr>
                                <th>Starts</th>
                                <th>Ends</th>
                                <th>View</th>
                            </tr>
                        </thead>
                        {pastAuctions.map((a, i) => (
                            <tr>
                                <td>{moment(a.start_time * 1000).fromNow()}</td>
                                <td>{moment(a.end_time * 1000).fromNow()}</td>
                                <td>
                                    <Button
                                        size="sm"
                                        onClick={() => history.push(`/auctions/${a.auction_id}`)}
                                    >
                                        View
                                    </Button>
                                </td>
                            </tr>
                        ))}
                    </Table>
                </Row>
            </Container>
            <ReportModal
                show={reportModalVisible}
                item_id={_id}
                handleClose={() => setReportModalVisible(false)}
            />
            <EditItemModal
                show={showEditItemModal}
                handleClose={() => setEditItemModalVisible(false)}
            />
            <CreateAuctionModal
                show={showCreateAuctionModal}
                handleClose={() => setCreateAuctionModalVisible(false)}
            />
            <WatchlistModal
                show={watchlistModalVisible}
                handleClose={() => setWatchlistModalVisible(false)}
            />
        </div>
    );
}
