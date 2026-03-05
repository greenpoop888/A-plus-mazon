import React, { useState, useEffect } from 'react';
import { Modal, List, Button, Icon, Header, Loader, Table, Pagination, Breadcrumb } from 'semantic-ui-react';

const MySubscriptionsModal = ({ isOpen, onClose }) => {
    const [view, setView] = useState('list'); // 'list' or 'files'
    const [selectedSub, setSelectedSub] = useState(null);
    const [loading, setLoading] = useState(false);

    // 模擬數據：訂閱項目
    const subscriptions = [
        { id: 101, title: 'Store 1 (By Minute)', type: 'store', target: 'Store 1', freq: 'minute' },
        { id: 102, title: 'Electronics (By Day)', type: 'category', target: 'Laptops', freq: 'day' },
    ];

    // 模擬數據：S3 檔案列表 (含分頁)
    const [files, setFiles] = useState([]);
    const [activePage, setActivePage] = useState(1);
    const totalPages = 5;

    const handleSubClick = (sub) => {
        setSelectedSub(sub);
        setLoading(true);
        // 這裡應該呼叫 API 獲取該訂閱下的 S3 檔案列表
        setTimeout(() => {
            setFiles([
                { id: 1, name: 'report_2026_03_04_1200.pdf', url: 'https://s3.amazon...' },
                { id: 2, name: 'report_2026_03_04_1201.pdf', url: 'https://s3.amazon...' },
            ]);
            setLoading(false);
            setView('files');
        }, 500);
    };

    const handleBack = () => {
        setView('list');
        setSelectedSub(null);
    };

    return (
        <Modal open={isOpen} onClose={onClose} size='small'>
            <Modal.Header>
                {view === 'files' && (
                    <Button icon='arrow left' basic size='mini' onClick={handleBack} style={{ marginRight: '1em' }} />
                )}
                {view === 'list' ? 'My Report Subscriptions' : `Reports for ${selectedSub?.title}`}
            </Modal.Header>

            <Modal.Content scrolling>
                {loading ? (
                    <Loader active inline='centered'>Fetching Reports...</Loader>
                ) : view === 'list' ? (
                    /* 視圖 1：訂閱項目清單 */
                    <List selection divided relaxed='very'>
                        {subscriptions.map(sub => (
                            <List.Item key={sub.id} onClick={() => handleSubClick(sub)}>
                                <Icon name='file alternate outline' color='blue' />
                                <List.Content>
                                    <List.Header>{sub.title}</List.Header>
                                    <List.Description>Target: {sub.target} | Frequency: {sub.freq}</List.Description>
                                </List.Content>
                                <List.Content floated='right'>
                                    <Icon name='chevron right' />
                                </List.Content>
                            </List.Item>
                        ))}
                    </List>
                ) : (
                    /* 視圖 2：檔案列表 (表格 + 分頁) */
                    <>
                        <Table basic='very' selectable>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell>Report Name</Table.HeaderCell>
                                    <Table.HeaderCell textAlign='right'>Action</Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>
                            <Table.Body>
                                {files.map(file => (
                                    <Table.Row key={file.id}>
                                        <Table.Cell>
                                            <Icon name='file pdf outline' color='red' /> {file.name}
                                        </Table.Cell>
                                        <Table.Cell textAlign='right'>
                                            <a href={file.url} target="_blank" rel="noreferrer">
                                                <Button size='mini' color='blue' icon='download' content='Download' />
                                            </a>
                                        </Table.Cell>
                                    </Table.Row>
                                ))}
                            </Table.Body>
                        </Table>

                        <div style={{ textAlign: 'center', marginTop: '1em' }}>
                            <Pagination
                                activePage={activePage}
                                onPageChange={(e, { activePage }) => setActivePage(activePage)}
                                totalPages={totalPages}
                                secondary
                            />
                        </div>
                    </>
                )}
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={onClose}>Close</Button>
            </Modal.Actions>
        </Modal>
    );
};

export default MySubscriptionsModal;