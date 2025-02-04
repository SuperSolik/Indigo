/****************************************************************************
 * Copyright (C) from 2009 to Present EPAM Systems.
 *
 * This file is part of Indigo toolkit.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ***************************************************************************/

#ifndef __ringo_core_c_parallel_h___
#define __ringo_core_c_parallel_h___

#include "bingo_core_c_internal.h"
#include "bingo_core_c_parallel.h"

#include "base_cpp/reusable_obj_array.h"

namespace indigo
{
    namespace bingo_core
    {

        class RingoIndexingCommandResult : public IndexingCommandResult
        {
        public:
            void clear() override;
            BingoIndex& getIndex(int index) override;

            ReusableObjArray<RingoIndex> per_reaction_index;
        };

        class RingoIndexingDispatcher : public IndexingDispatcher
        {
        public:
            RingoIndexingDispatcher(BingoCore& core);

        protected:
            void _exposeCurrentResult(int index, IndexingCommandResult& result) override;
            OsCommandResult* _allocateResult() override;
        };

    } // namespace bingo_core
} // namespace indigo

#endif // __mango_core_c_parallel_h___
