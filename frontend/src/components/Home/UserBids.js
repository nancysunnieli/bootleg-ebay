import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getItemsBySeller } from "../../slices/items";
import Spinner from "react-bootstrap/Spinner";
import { ScrollMenu, VisibilityContext } from "react-horizontal-scrolling-menu";
import ItemCard from "../Items/ItemCard";
import { getUserBids } from "../../slices/auctions";
import Table from "react-bootstrap/Table";
import { useHistory } from "react-router-dom";
import Button from "react-bootstrap/Button";
import moment from "moment";
const UserBids = () => {
    const { user } = useSelector((state) => state.auth);
    const { userBids, getUserBidsLoading } = useSelector((state) => state.auctions);
    const dispatch = useDispatch();
    const history = useHistory();

    useEffect(() => {
        dispatch(getUserBids({ user_id: user.user_id }));
    }, []);

    if (getUserBidsLoading) {
        return <Spinner animation="grow" variant="success" />;
    }

    let tbody = userBids.flatMap((ub, i) => {
        let isEnded = ub.auction.end_time * 1000 < new Date().getTime();
        return ub.user_bids.map((bid, j) => (
            <tr key={`${bid.bid_id}_${i}_${j}`}>
                <td>{ub.item.name}</td>
                <td>{bid.price}</td>
                <td key={bid.bid_time}>{new Date(bid.bid_time * 1000).toLocaleString()}</td>
                <td>{isEnded ? "Ended" : new Date(ub.auction.end_time * 1000).toLocaleString()}</td>
                <td>
                    <Button onClick={() => history.push(`/items/${ub.item._id}`)}>View</Button>
                </td>
            </tr>
        ));
    });
    tbody.sort((a, b) => parseFloat(b.props.children[2].key) - parseFloat(a.props.children[2].key));

    return (
        <div style={{ position: "relative" }}>
            <Table striped hover responsive="sm">
                <thead>
                    <tr>
                        <th>Item Name</th>
                        <th>Bid Price</th>
                        <th>Bid Time</th>
                        <th>Auction Ends On</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>{tbody}</tbody>
            </Table>
        </div>
    );
};

export default UserBids;
