/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canMap from 'can-map';
import canComponent from 'can-component';
import * as businessModels from '../../../models/business-models';
import {loadObjectsByTypes} from '../../../plugins/utils/query-api-utils';
import {notifier} from '../../../plugins/utils/notifiers-utils';
import {getAjaxErrorInfo} from '../../../plugins/utils/errors-utils';
import {getRelevantMappingTypes} from '../../../plugins/utils/workflow-utils';

/**
 * @typedef {Object} Stub
 * @property {number} id - id of a pre-mapped object
 * @property {string} type - type of a pre-mapped object
 */

const viewModel = canMap.extend({
  instance: null,
  isNewInstance: false,
  /**
  * @type {Cacheable[]}
  */
  mappedObjects: [],
  /**
  * @type {Stub[]}
  */
  preMappedStubs: [],
  /**
  * @type {Cacheable[]}
  */
  preMappedObjects: [],
  isLoading: false,
  loadPreMappedObjects() {
    return this.attr('preMappedStubs').map((stub) =>
      businessModels[stub.type].findInCacheById(stub.id)
    );
  },
  loadMappedObjects() {
    const instance = this.attr('instance');
    const fields = ['id', 'type', 'title'];
    return loadObjectsByTypes(
      instance,
      getRelevantMappingTypes(instance),
      fields
    );
  },
  async init() {
    this.attr('preMappedObjects', this.loadPreMappedObjects());

    if (this.attr('isNewInstance')) {
      return;
    }

    this.attr('isLoading', true);
    try {
      this.attr('mappedObjects', await this.loadMappedObjects());
    } catch (xhr) {
      notifier('error', getAjaxErrorInfo(xhr).details);
    } finally {
      this.attr('isLoading', false);
    }
  },
});

export default canComponent.extend({
  tag: 'cycle-task-modal',
  leakScope: true,
  viewModel,
});
